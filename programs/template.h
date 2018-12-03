#include <time.h>

#define TRUE  1
#define FALSE 0
#define ENDS  ('\0')

// Random Numbers

#define RANDMAX (100)
#define RANDINIT (time(NULL)) // can be 0 also

int getrandom()
{
    static int randinit = FALSE;
    if (!randinit) {
	srand(RANDINIT);
	randinit = TRUE;
    }
    return rand()%RANDMAX;
}


// Arguments

void printargs(int argc, char *argv[])
{
    int c;
    for (c = 0; c < argc; ++c) {
	printf("%s ", argv[c]);
    }
    printf("(%d)\n", argc);
}


void load(unsigned int i)
{
    while(--i);
}

// Run Time Tracking

clock_t _tsall_ = 0;
clock_t _tscur_ = 0;
int trackonstate = FALSE;

void trackon()
{
    if (trackonstate)
	return;

    _tsall_ = 0;
    _tscur_ = clock();
    trackonstate = TRUE;
}

void trackoff()
{
    if (!trackonstate)
	return;

    trackonstate = FALSE;
    _tscur_ = clock() - _tscur_;
    _tsall_ += _tscur_;
}

void trackprint()
{
    int trackerwason = trackonstate;
    trackoff();

    printf("Runtime: %f seconds\n", ((double)_tsall_) / CLOCKS_PER_SEC); 

    if (trackerwason)
    trackon();
}


