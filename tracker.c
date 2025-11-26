#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <dlfcn.h>
#include <unistd.h>
#include <fcntl.h>  // <--- Added this

// Pointers to the real memory functions
static void *(*real_malloc)(size_t) = NULL;
static void (*real_free)(void *) = NULL;

// <--- Added this function: Clears the log file when the program starts
void __attribute__((constructor)) init() {
    FILE *fp = fopen("memory.log", "w");
    if (fp) fclose(fp);
}

// Hook for malloc
void *malloc(size_t size) {
    if (!real_malloc) {
        real_malloc = dlsym(RTLD_NEXT, "malloc");
    }

    void *p = real_malloc(size);

    // Open log file in append mode
    FILE *fp = fopen("memory.log", "a");
    if (fp) {
        fprintf(fp, "ALLOC %zu\n", size);
        fclose(fp);
    }
    return p;
}

// Hook for free
void free(void *p) {
    if (!real_free) {
        real_free = dlsym(RTLD_NEXT, "free");
    }
    
    real_free(p);
    
    // We log '0' size to represent a free event for now
    FILE *fp = fopen("memory.log", "a");
    if (fp) {
        fprintf(fp, "FREE 0\n");
        fclose(fp);
    }
}