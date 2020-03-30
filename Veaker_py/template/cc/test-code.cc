#include "{{target}}.h"

#include <cstring>
#include <iostream>

{% for header in headers %}#include "{{header}}.h"
{% endfor %}
void
unittest(int argc, const char **argv) {
    
    {{target}}();
}

void
integrationtest(int argc, const char **argv) {
    
    {{target}}();
}

int
main(int argc, const char **argv){
    if (argc < 2) {
        std::cerr << "Few arguments!" << std::endl;
        return 1;
    }

    if (strcmp(argv[1], "unit") == 0) {
        unittest(argc, argv);
    } else if (strcmp(argv[1], "integration") == 0) {
        integrationtest(argc, argv);
    } else {
        std::cerr << "Unknown option!" << std::endl;
        return 1;
    }

    return 0;
}
