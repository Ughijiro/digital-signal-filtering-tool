// Purpose: Test the UART receiver on the laptop.

#include <stdio.h>
#include <stdint.h>


// Functions implemented in uart_receiver.c
void readRX(uint8_t byte);
int uart_get_checksum_status(void);
int uart_get_b_count(void);
int uart_get_a_count(void);
double uart_get_b(uint8_t index);
double uart_get_a(uint8_t index);
uint32_t uart_get_valid_messages(void);

int main(int argc, char *argv[])
{
    // Open the binary UART message.
    const char *packet_path = argc > 1 ? argv[1] : "tests/packet.bin";

    FILE *file = fopen(packet_path, "rb");
    if (file == NULL) {
        printf("Error opening packet.bin\n");
        return 1;
    }

    printf("File opened successfully\n");

    int byte;

    while ((byte = fgetc(file)) != EOF) {
        // Procesăm octetul primit
        readRX((uint8_t)byte);
    }
    printf("Valid messages: %u\n",
       (unsigned int)uart_get_valid_messages());

    int b_count = uart_get_b_count();
    int a_count = uart_get_a_count();

    printf("Checksum valid: %d\n", uart_get_checksum_status());
    printf("B count: %d\n", b_count);
    printf("A count: %d\n", a_count);

    printf("B coefficients:\n");
    for(int i = 0; i < b_count; i++){
        printf("Coefficient #%d: %.17g\n", i, uart_get_b(i));
    }
    
    printf("A coefficients:\n");
    for(int i = 0; i < a_count; i++){
        printf("Coefficient #%d: %.17g\n", i, uart_get_a(i));
    }
    
    fclose(file);
    
    FILE *reference = fopen(
        "tests/coefficients_reference.txt", "r"
    );

    if (reference == NULL) {
        printf("Error opening coefficients_reference.txt\n");
        return 1;
    }

    if (!uart_get_checksum_status()) {
        printf("Invalid UART packet\n");
        fclose(reference);
        return 1;
    }

    int errors = 0;

    for (int i = 0; i < b_count; i++) {
        double expected;

        if (fscanf(reference, "%lf", &expected) != 1) {
            printf("Error reading reference coefficient\n");
            fclose(reference);
            return 1;
        }

        double actual = uart_get_b(i);

        if (actual != expected) {
            errors++;
            printf("Mismatch at b[%d]\n", i);
        }
    }
    
    for (int i = 0; i < a_count; i++) {
        double expected;

        if (fscanf(reference, "%lf", &expected) != 1) {
            printf("Error reading reference coefficient\n");
            fclose(reference);
            return 1;
        }

        double actual = uart_get_a(i);

        if (actual != expected) {
            errors++;
            printf("Mismatch at a[%d]\n", i);
        }
    }
    
    fclose(reference);

    if (errors == 0) {
        printf("\nCoefficient comparison: PASS\n");
    }
    else {
        printf("\nCoefficient comparison: FAIL\n");
        printf("Mismatches: %d\n", errors);
        return 1;
    }
    return 0;
}