#include <stdio.h>
#include <string.h>

#define BUFFER_SIZE 10


void vulnerable_function() {
    char buffer[BUFFER_SIZE];
    printf("Enter string: ");
    gets(buffer);  // Attention! gets() is unsave.
    
    printf("Entered string: %s\n", buffer);
}

void safe_function() {
    char buffer[BUFFER_SIZE];
    printf("Enter string: ");
    if (fgets(buffer, sizeof(buffer), stdin) == NULL) {
        perror("Input error");
        return;
    }

    buffer[strcspn(buffer, "\n")] = 0;
    printf("Entered string: %s\n", buffer);
}

int main() {
    int choice;

    printf("Enter string input variant:\n");
    printf("1. Unsafe input\n");
    printf("2. Safe input\n");
    scanf("%d", &choice);
    
    while (getchar() != '\n');

    if (choice == 1) {
        printf("Launch unsafe code:\n");
        vulnerable_function();
    } else if (choice == 2) {
        printf("Launch safe code:\n");
        safe_function();
    } else {
        printf("Please. Enter 1 or 2\n");
    }

    return 0;
}
