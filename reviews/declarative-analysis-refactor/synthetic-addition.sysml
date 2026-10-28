package AdditionalStudy {
    part candidate : DeclarativeStudyFixtures::Configuration {
        attribute :>> capacity = 35;
        attribute :>> label = "Added synthetic configuration";
    }
    analysis configured : DeclarativeStudyFixtures::Scale {
        subject :>> target = candidate;
        in attribute :>> gain = 3;
    }
}
