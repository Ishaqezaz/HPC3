#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int main(int argc, char *argv[]) {
    int rank, size, i;
    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    int nxc = 128;
    double L = 2 * M_PI;
    int nxn_loc = nxc / size + 2;
    double dx = L / (double)nxc;

    double *f = calloc(nxn_loc, sizeof(double));
    double *dfdx = calloc(nxn_loc, sizeof(double));

    for (i = 1; i < nxn_loc - 1; i++) {
        f[i] = sin(dx * (rank * (nxn_loc - 2) + (i - 1)));
    }

    int left = (rank == 0) ? size - 1 : rank - 1;
    int right = (rank == size - 1) ? 0 : rank + 1;

    MPI_Request sendRequest[2];
    MPI_Request recvRequests[2];

    MPI_Isend(&f[nxn_loc - 2], 1, MPI_DOUBLE, right, 0, MPI_COMM_WORLD, &sendRequest[0]);
    MPI_Irecv(&f[0], 1, MPI_DOUBLE, left, 0, MPI_COMM_WORLD, &recvRequests[0]);
    MPI_Isend(&f[1], 1, MPI_DOUBLE, left, 1, MPI_COMM_WORLD, &sendRequest[1]);
    MPI_Irecv(&f[nxn_loc - 1], 1, MPI_DOUBLE, right, 1, MPI_COMM_WORLD, &recvRequests[1]);

    MPI_Waitall(2, sendRequest, MPI_STATUSES_IGNORE);
    MPI_Waitall(2, recvRequests, MPI_STATUSES_IGNORE);

    for (i = 1; i < nxn_loc - 1; i++) {
        dfdx[i] = (f[i + 1] - f[i - 1]) / (2 * dx);
    }

    MPI_Barrier(MPI_COMM_WORLD);
    double ghostLeft = sin(dx * ((rank * (nxn_loc - 2) - 1) % nxc));
    double ghostRight = sin(dx * (((rank + 1) * (nxn_loc - 2)) % nxc));
    double primLeft = cos(dx * (rank * (nxn_loc - 2)));
    double primRight = cos(dx * ((rank + 1) * (nxn_loc - 2) - 1));

    printf("Rank %d of %d\n", rank, size);
    printf("Ghost cell on the left should be: %f, and is %f\n", ghostLeft, f[0]);
    printf("Ghost cell on the right should be: %f, and is %f\n", ghostRight, f[nxn_loc - 1]);
    printf("Derivative on the left boundary should be: %f, and is %f\n", primLeft, dfdx[1]);
    printf("Derivative on the right boundary should be: %f, and is %f\n", primRight, dfdx[nxn_loc - 2]);

    free(f);
    free(dfdx);
    MPI_Finalize();
    return 0;
}

