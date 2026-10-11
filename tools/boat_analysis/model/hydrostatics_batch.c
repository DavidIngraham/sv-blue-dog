/* Batching only: tetra clipping equations are generated from hydrostatics.sysml. */
#include "hydrostatics.c"
int hydro_mesh(double *vertices, int64_t count, double waterline, double *result) {
    for (int j=0;j<4;j++) result[j]=0;
    for (int64_t i=0;i<count;i++) {
        sysml_seq_real p={SYSML_MANY,12,vertices+12*i}, out;
        if (sysml_run(p,waterline,&out)) return 1;
        if (out.shape!=SYSML_MANY || out.len!=4) return 2;
        for (int j=0;j<4;j++) result[j]+=out.data[j];
    }
    return 0;
}
