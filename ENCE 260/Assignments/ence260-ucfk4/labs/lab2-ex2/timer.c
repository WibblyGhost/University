#include <avr/io.h>
#include "timer.h"

/* Initialise timer.  */
void timer_init (void)
{
    /* TODO */
    TCCR1A = 0x00;
    TCCR1B = 0x05;
    TCCR1C = 0x00;
}


/* Wait for the specified length of time.  */
void timer_delay_ms (uint16_t milliseconds)
{

    /* TODO: Calculate the timer/counter value needed 
       for the given number of milliseconds. */
    unsigned int increments = 0;
    increments = milliseconds / (1000 * 0.000128);
    TCNT1 = 0x00;


    /* TODO: Wait for the timer/counter to reach the
       value calculated above.  */
    while (TCNT1 < increments) {
        continue;
    }

}
