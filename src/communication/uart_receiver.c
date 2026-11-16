// Purpose: Receive and validate UART messages
// containing Butterworth filter coefficients.

#include <stdint.h>
#include <string.h>

#define MAX_PAYLOAD_SIZE 144

typedef enum {
    WAIT_AA,
    WAIT_BB,
    WAIT_CC,
    WAIT_DD,
    READ_COUNTS,
    READ_PAYLOAD,
    READ_CHECKSUM
} UartState;

static UartState state = WAIT_AA;
static uint8_t b_count = 0;
static uint8_t a_count = 0;
static uint8_t count_index = 0;
static uint16_t expected_payload_bytes = 0;
static uint8_t rx_buffer[MAX_PAYLOAD_SIZE];
static uint16_t rx_index = 0;
static uint8_t calculated_checksum = 0;
static uint8_t checksum_ok = 0;
static uint32_t valid_messages = 0;

// Purpose: Return the checksum verification result.
int uart_get_checksum_status(void)
{
    return checksum_ok;
}

int uart_get_b_count(void)
{
    return checksum_ok ? b_count : 0;
}

int uart_get_a_count(void)
{
    return checksum_ok ? a_count : 0;
}

uint32_t uart_get_valid_messages(void)
{
    return valid_messages;
}

void readRX(uint8_t byte)
{
    switch(state){
        case WAIT_AA:
            if(byte == 0xAA){
                calculated_checksum = 0;
                rx_index = 0;
                count_index = 0;
                checksum_ok = 0;
                state = WAIT_BB;
            }
            break;
        case WAIT_BB:
            if(byte == 0xBB){
                state = WAIT_CC;
            }
            else{
                state = WAIT_AA;
            }
            break;
        case WAIT_CC:
            if(byte == 0xCC){
                state = WAIT_DD;
            }
            else{
                state = WAIT_AA;
            }
            break;
        case WAIT_DD:
            if(byte == 0xDD){
                state = READ_COUNTS;
            }
            else{
                state = WAIT_AA;
            }
            break;
        case READ_COUNTS:
            if (count_index == 0)
            {
                b_count = byte;
                calculated_checksum += byte;
                count_index = 1;
            }
            else
            {
                a_count = byte;
                calculated_checksum += byte;
                count_index = 0;
                expected_payload_bytes = (a_count + b_count)*8;

                if(expected_payload_bytes > MAX_PAYLOAD_SIZE || 
                    a_count == 0 || b_count == 0)
                {
                    state = WAIT_AA;
                    rx_index = 0;
                    break;
                }

                state = READ_PAYLOAD;
            }
            break;
        case READ_PAYLOAD:
            if (rx_index < expected_payload_bytes) {
                rx_buffer[rx_index] = byte;
                rx_index++;
                calculated_checksum += byte;
                if(rx_index == expected_payload_bytes){
                    state = READ_CHECKSUM;
                }
            }
            break;
        case READ_CHECKSUM:
            if (byte == calculated_checksum) {
                checksum_ok = 1;
                valid_messages++;
            }
            else {
                checksum_ok = 0;
            }

            state = WAIT_AA;
            break;
    }
}

// Purpose: Reconstruct a b coefficient by its index.
double uart_get_b(uint8_t index)
{
    double value = 0.0;

    if (!checksum_ok || index >= b_count || sizeof(double) != 8)
        return 0.0;

    size_t offset = index * 8;

    memcpy(&value, rx_buffer + offset, 8);

    return value;
}

// Purpose: Reconstruct an a coefficient by its index.
double uart_get_a(uint8_t index)
{
    double value = 0.0;

    if (!checksum_ok || index >= a_count || sizeof(double) != 8)
        return 0.0;

    // Calculate offset.
    // Copy 8 bytes into value.
    size_t offset = (b_count + index) * 8;
    memcpy(&value, rx_buffer + offset, 8);

    return value;
}