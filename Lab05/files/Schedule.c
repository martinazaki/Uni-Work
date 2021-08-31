// Schedule ADT implementation

#include <stdio.h>
#include <stdlib.h>

#include "Schedule.h"
#include "Time.h"
#include "Tree.h"

struct schedule {
    Tree times;
    int  count;
};

// Creates a new schedule
Schedule ScheduleNew(void) {
    Schedule s = malloc(sizeof(*s));
    if (s == NULL) {
        fprintf(stderr, "Insufficient memory!\n");
        exit(EXIT_FAILURE);
    }

    s->times = TreeNew();
    s->count = 0;
    return s;
}

// Frees all memory associated with a given schedule
void ScheduleFree(Schedule s) {
    TreeFree(s->times);
    free(s);
}

// Gets the number of times added to the schedule
int  ScheduleCount(Schedule s) {
    return s->count;
}

// Attempts to schedule a new landing time. Returns true if the time was
// successfully added, and false otherwise.
bool ScheduleAdd(Schedule s, Time t) {
    if (s->times == NULL) {
        return false;
    }

    Time floorTime = NULL;
    floorTime = TreeFloor(s->times, t);

    Time ceilingTime = NULL;
    ceilingTime = TreeCeiling(s->times, t);

    if (ceilingTime == NULL && floorTime == NULL) {
        //Insert new schedule into tree
        TreeInsert(s->times, t);
        s->count++;
        return true;

    }

    else if (ceilingTime != NULL && floorTime != NULL) {
        if (TimeCmp(t, ceilingTime) >= 0 || TimeCmp(t, floorTime) <= 0) {
            return false;
        }
        //Insert new schedule into tree
        TreeInsert(s->times, t);
        s->count++;
        return true;

    }

    else if (ceilingTime == NULL && floorTime != NULL) {
        floorTime = TimeAddMinutes(floorTime, 10);
        if (TimeCmp(t,floorTime) <= 0) {
            return false;
        }
        //Insert new schedule into tree
        TreeInsert(s->times, t);
        s->count++;
        return true;

    }

    else if (ceilingTime != NULL && floorTime == NULL) {
        ceilingTime = TimeSubtractMinutes(ceilingTime, 10);
        if (TimeCmp(t, ceilingTime) >= 0) {
            return false;
        }
        //Insert new schedule into tree
        TreeInsert(s->times, t);
        s->count++;
        return true;

    }
    //Insert new schedule into tree
    TreeInsert(s->times, t);
    s->count++;
    return true;
}

// Shows  all  the landing times in the schedule. If mode is 1, only the
// times are shown. If mode is 2, the underlying data structure is shown
// as well.
void ScheduleShow(Schedule s, int mode) {
    if (mode == 1) {
        TreeList(s->times);
    } else if (mode == 2) {
        TreeShow(s->times);
    }
}
