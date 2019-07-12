#include <avr/io.h>
#include "button.h"


/** Return non-zero if button pressed.  */
int button_pressed_p (void)
{
    /* TODO.  */
    if (PIND & 1<<7) {
        return 1;
    } else {
        return 0;
    }
}


/** Initialise button1.  */
void button_init (void)
{
    /* TODO.  */
    DDRD &= 0<<7;
}

