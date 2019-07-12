#include <avr/io.h>
#include "system.h"

int main (void)
{
    system_init ();

    /* Initialise port to drive LED 1.  */
    DDRC |= 1<<2;
    /* TODO.  */

    while (1)
    {

        /* Turn LED 1 on.  */
        PORTC |= 1<<2;
        /* TODO.  */

    }
}
