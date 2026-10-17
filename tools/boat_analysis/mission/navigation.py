"""Observed-track transport to native Inland rule and candidate assessments.

Geometry is numerical; all role, memory and candidate permission decisions are
native SysML. Missing assessed facts stay unknown. No future truth is accepted.
"""
from collections import Counter
from functools import lru_cache
import math
import numpy as np
from opensysml import EnumLiteral
from ..model.runtime import ROOT, load_model

SOURCES = (ROOT/'models/libraries/navigation/inland-pair.sysml',
           ROOT/'models/analyses/navigation-controller.sysml')

@lru_cache(maxsize=1)
def rule_model():
    return load_model(SOURCES)

@lru_cache(maxsize=8)
def interface(name):
    return {s.name:s.type_facts for s in rule_model().find(name).children()
            if s.metadata.get('direction') == 'in'}

@lru_cache(maxsize=8192)
def _evaluate(name, items):
    kinds=interface(name)
    if set(dict(items)) != set(kinds):
        raise ValueError('Native navigation assessment requires every input')
    args={k:EnumLiteral(kinds[k].resolved_id+'::'+v,kinds[k].resolved_id)
          if kinds[k].resolved_kind=='enumDef' else v for k,v in items}
    outputs=rule_model().run_analysis(name, subject=name.rsplit('::',1)[0]+'::context', named_arguments=args).outputs
    return {k:v.literal_id.rsplit('::',1)[-1] if isinstance(v,EnumLiteral) else v for k,v in outputs.items()}

def evaluate(name, **inputs):
    return dict(_evaluate(name,tuple(sorted(inputs.items()))))

def truth(value):
    return 'yes' if value else 'no'

def angle(a,b):
    return abs((a-b+180)%360-180)

def bearing(vector, heading):
    return angle(math.degrees(math.atan2(vector[1],vector[0])),heading)

def trajectory_clear(actor, position, seconds, segments, dimensions):
    """Exact linear segments against the delivered constant-velocity track."""
    start=np.asarray(position,dtype=float)
    now=seconds
    for duration,velocity in segments:
        if duration <= 0:continue
        end=start+np.asarray(velocity)*duration
        safe,_=actor.assess(start,np.array([end]),now,duration,duration,dimensions)
        if not safe[0]:return False
        start=end;now+=duration
    return True


_UNSET=object()

class NavigationAssessment:
    def __init__(self, *, assessed_context=None, label='unassessed'):
        self.context=dict(assessed_context or {})
        self.label=label
        self.policy=evaluate('BlueDogNavigationController::Policy')
        self.memory={}
        self.approved={}
        self.latest={}
        self.trace=[]
        self.last_signature={}
        self.gaps=Counter()
        self.roles=Counter()
        self.cycles=0
        self.filtered=0
        self.changed=0
        self.last_allowed=None
        self.recovery_unassessed=False

    def _record(self, seconds, identity, row):
        signature=tuple((k,str(v)) for k,v in row.items() if k not in {'rangeM'})
        if self.last_signature.get(identity)!=signature:
            self.trace.append(dict(seconds=float(seconds),actorId=identity,**row))
            self.last_signature[identity]=signature

    def assess(self, *, position, contacts, seconds, interval, forecast, dimensions,
               headings, endpoints, velocities, held_velocity, heading, permitted, committed=False, trajectories=None, reference_trajectory=None, motion_velocity=None, assessment_heading=_UNSET):
        self.cycles+=1
        motion_velocity=held_velocity if motion_velocity is None else motion_velocity
        assessed_heading=heading if assessment_heading is _UNSET else assessment_heading
        self.latest={}
        context=evaluate('BlueDogNavigationController::Context',inlandProfile=self.context.get('inlandProfile','unknown'),
            channelContext=self.context.get('channelContext','unknown'),restrictedVisibility=self.context.get('restrictedVisibility','unknown'),
            specialCircumstances=self.context.get('unmodeledSpecialCircumstances','unknown'))
        if not context['supported']:
            self.gaps['controller_context_not_supported']+=1
            self._record(seconds,'context',dict(response='unresolved',reason='controller_context_not_supported'))
            self.last_allowed=np.zeros(len(permitted),dtype=bool)
            return self.last_allowed.copy()
        allowed=np.array(permitted,dtype=bool,copy=True)
        ids={a.source_id for a in contacts if a.source_id is not None}
        missing=any(state!='clear' and identity not in ids for identity,state in self.memory.items())
        if missing:
            self.gaps['lost_track_with_active_overtaking_duty']+=1
            self._record(seconds,'missing',dict(response='unresolved',reason='lost_track_with_active_overtaking_duty'))
        for index,actor in enumerate(contacts):
            if trajectories is not None:
                for j in np.flatnonzero(allowed):
                    allowed[j] &= trajectory_clear(actor,position,seconds,trajectories[j],dimensions)
            # Weed is an observed obstacle class, never a vessel priority claim.
            if actor.target_kind=='weed':continue
            identity=actor.source_id if actor.source_id is not None else index
            facts=actor.navigation_facts
            relative=actor.position(seconds)-position
            distance=float(np.linalg.norm(relative))
            other_velocity=(actor.position(seconds+1)-actor.position(seconds))
            own_speed=float(np.linalg.norm(held_velocity))
            other_speed=float(np.linalg.norm(other_velocity))
            closing=float(-relative@(other_velocity-motion_velocity)/max(distance,1e-9))
            held_endpoint=position+held_velocity*forecast
            held_safe,held_penalty=actor.assess(position,np.array([held_endpoint]),seconds,forecast,forecast,dimensions)
            held_clear=bool(held_safe[0] and held_penalty[0]==0)
            if reference_trajectory is not None:
                held_clear=held_clear and trajectory_clear(actor,position,seconds,reference_trajectory,dimensions)
            memory=self.memory.get(identity,'clear')
            relevant=not held_clear or memory!='clear' or self.context.get('channelContext','unknown')!='no' or self.context.get('unmodeledSpecialCircumstances','unknown')!='no'
            if not relevant:
                continue
            protected=math.hypot(dimensions[0],dimensions[1])/2+math.hypot(actor.length_m,actor.beam_m)/2+actor.clearance_m
            known=assessed_heading is not None and other_speed>1e-6
            other_heading=math.degrees(math.atan2(other_velocity[1],other_velocity[0])) if other_speed>1e-6 else 0.
            own_bearing=bearing(-relative,other_heading) if known else 90.
            other_bearing=bearing(relative,assessed_heading) if known else 90.
            uncertainty=float(self.policy['bearingUncertaintyDeg'])
            geometry=dict(rangeM=distance,closingMps=closing,protectedRadiusM=protected,
                releaseMultiplier=float(self.policy['clearanceReleaseMultiplier']),heldConflict=not held_clear,
                headingKnown=heading is not None,trackAdequate=facts.get('observationsAdequate','unknown')=='yes',
                headingToleranceDeg=float(self.policy['headingToleranceDeg']),speedToleranceMps=float(self.policy['speedToleranceMps']),
                substantialTurnDeg=float(self.policy['substantialTurnDeg']))
            release=evaluate('BlueDogNavigationController::Geometry',**geometry,headingChangeDeg=0.,speedChangeMps=0.)
            side='unresolved' if heading is None else ('starboardSide' if (math.degrees(math.atan2(relative[1],relative[0]))-heading+180)%360-180<0 else 'portSide')
            data=dict(inlandProfile=self.context.get('inlandProfile','unknown'),inSight=facts.get('inSight','unknown'),
                restrictedVisibility=self.context.get('restrictedVisibility','unknown'),riskOfCollision=truth(not held_clear),
                ownKind=self.context.get('ownKind','sailing'),otherKind=facts.get('kind','unclassified'),
                ownExceptionalStatus=self.context.get('ownExceptionalStatus','unknown'),otherExceptionalStatus=facts.get('exceptionalStatus','unknown'),
                unmodeledSpecialCircumstances=self.context.get('unmodeledSpecialCircumstances','unknown'),
                observationsAdequate=facts.get('observationsAdequate','unknown'),lookoutAdequate=self.context.get('lookoutAdequate','unknown'),
                safeSpeedSupported=self.context.get('safeSpeedSupported','unknown'),ownTack=self.context.get('ownTack','unresolved'),
                otherTack=facts.get('tack','unresolved'),windward=facts.get('windward','unresolved'),
                ownComingUp=truth(closing>0) if known else 'unknown',otherComingUp=truth(closing>0) if known else 'unknown',
                ownBearingLowDeg=max(0.,own_bearing-uncertainty),ownBearingHighDeg=min(180.,own_bearing+uncertainty),
                otherBearingLowDeg=max(0.,other_bearing-uncertainty),otherBearingHighDeg=min(180.,other_bearing+uncertainty),
                declaredOwnOvertakingDoubt='no' if known else 'unknown',previousMemory=memory,
                pastAndClear=truth(release['pastAndClear']),clearanceEvidenceAdequate=truth(release['pastAndClear']),
                otherActionAppropriate=facts.get('otherActionAppropriate','unknown'),
                giveWayAloneSufficient=facts.get('giveWayAloneSufficient','unknown'),ownAvoidanceFeasible='unknown',
                immediateDanger='unknown' if not known else truth(distance<=protected),
                channelContext=self.context.get('channelContext','unknown'),otherConfinedToChannel=facts.get('confinedToChannel','unknown'),
                ownLengthM=float(dimensions[0]),crossingChannel=self.context.get('crossingChannel','unknown'),
                crossingWouldImpede='unknown',proceedingAlongChannel=self.context.get('proceedingAlongChannel','unknown'),
                channelPlanSupported=self.context.get('channelPlanSupported','unknown'),powerEncounter='uncertain',
                targetSide=side,headOnDoubt='unknown',passageAgreement='none',specialRiverRulesApply=self.context.get('specialRiverRulesApply','unknown'),
                ownRiverMotion='unresolved',otherRiverMotion='unresolved',downboundFollowingCurrent='unknown',
                ownUnderway='yes',otherUnderway=facts.get('underway','unknown'),portTurnProposed='unknown',
                crossAheadProposed='unknown',circumstancesAdmit='unknown',otherNavigatingChannel=facts.get('navigatingChannel','unknown'),starboardTurnProposed='unknown')
            # Candidate-independent result advances memory exactly once per observed pair.
            base=evaluate('InlandNavigationExperiment::Assess',**data)
            self.memory[identity]=base['nextMemory']
            self.roles[base['role']]+=1
            self.latest[identity]=(base['role'],base['response'])
            gaps=[]
            for key in ('inSight','observationsAdequate','lookoutAdequate','safeSpeedSupported','channelContext','ownExceptionalStatus','otherExceptionalStatus','unmodeledSpecialCircumstances'):
                if data[key]=='unknown':gaps.append(key)
            if data['otherKind']=='unclassified':gaps.append('vessel_status')
            if base['response']=='unresolved':gaps.append('encounter_response')
            if base['rule19AssessmentNeeded']:gaps.append('restricted_visibility_controller')
            if base['nonImpedimentDuty']!='no':gaps.append('channel_plan_or_applicability')
            self.gaps.update(gaps)
            safe,penalty=actor.assess(position,endpoints,seconds,interval,forecast,dimensions)
            rejected=0
            for j in np.flatnonzero(allowed):
                candidate_clear=bool(safe[j] and penalty[j]==0)
                if trajectories is not None:
                    candidate_clear=candidate_clear and trajectory_clear(actor,position,seconds,trajectories[j],dimensions)
                proposed=None if math.isnan(headings[j]) else float(headings[j])
                delta=0. if heading is None or proposed is None else (proposed-heading+180)%360-180
                g=evaluate('BlueDogNavigationController::Geometry',**dict(geometry,headingKnown=heading is not None and proposed is not None),
                    headingChangeDeg=abs(delta),
                    speedChangeMps=abs(float(np.linalg.norm(velocities[j]))-own_speed))
                candidate=dict(data,ownAvoidanceFeasible=truth(candidate_clear),portTurnProposed=truth(delta>0),
                               starboardTurnProposed=truth(delta<0))
                result=evaluate('InlandNavigationExperiment::Assess',**candidate)
                decision=evaluate('BlueDogNavigationController::Candidate',relevant=relevant,
                    supported=result['selectionSupported'],candidateClear=candidate_clear,heldClear=held_clear,
                    holdsCourseSpeed=g['holdsCourseSpeed'],substantialChange=g['substantialChange'],
                    missingTrackedDuty=missing,response=result['response'],
                    continuationSupported=committed and self.approved.get(identity)==(result['role'],result['response']))
                if not decision['allowed']:allowed[j]=False;rejected+=1
            self._record(seconds,identity,dict(actor=actor.name,rangeM=distance,role=base['role'],response=base['response'],
                ruleBasis=base['ruleBasis'],memory=base['nextMemory'],gaps=sorted(gaps),rejectedCandidates=rejected,
                candidateAvailable=bool(allowed.any()),factsSource=facts.get('source','unassessed')))
        if missing:
            allowed[:]=False
        self.filtered+=int(np.sum(np.asarray(permitted,dtype=bool)&~allowed))
        self.last_allowed=allowed.copy()
        return allowed

    def selected(self, original, actual):
        if self.last_allowed is not None and self.last_allowed[actual]:
            self.changed+=int(original!=actual)
            self.approved=dict(self.latest)

    def summary(self):
        return dict(enabled=True,label=self.label,decisionCycles=self.cycles,filteredCandidates=self.filtered,
            changedSelections=self.changed,roles=dict(self.roles),unresolvedObligations=dict(self.gaps),
            activeOvertakingMemory=dict(self.memory),trace=self.trace,completeComplianceEstablished=False,
            recoveryNavigationAssessed=False,policy={k:float(v) for k,v in self.policy.items()},
            contextAssumptions=self.context,
            scope='Observed-track pair assessment filters primary sailing candidates. Kinematic forecast, qualitative judgments, rig tack, multi-vessel negotiation, Rule 19 control, equipment and recovery navigation remain unqualified.')
