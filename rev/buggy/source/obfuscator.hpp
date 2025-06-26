/*
* took this from the vxug paper about constexpr
*/

#ifndef OBFUSCATOR_HPP__
#define OBFUSCATOR_HPP__

#ifdef _MSC_VER
#pragma warning(push)
#pragma warning(disable: 4996)
#endif

namespace ob {

#define KEY 0x55

     /*
      * a simple xor will just be detected by floss, this works better
      */
    constexpr char obfuscatedXor(char a, char b) {
        return ((~((((~a) & 0xFF) | b) & (a | ((~b) & 0xFF)))) & 0xFF) &
            (((~((((~a) & 0xFF) | b) & (a | ((~b) & 0xFF)))) & 0xFF) |
                (char)(0xB7F748F3));
    }

    /*
     * obfuscator is a class that helps with the storage of encrypted strings
     * and their decryption.
     */
    template <unsigned int N>
    struct obfuscator {
        /*
         * m_data stores the obfuscated string.
         */
        char m_data[N] = { 0 };

        /*
         * Using constexpr ensures that the strings will be obfuscated in this
         * constructor function at compile time.
         */
        constexpr obfuscator(const char* data) {
            /*
             * Implement encryption algorithm here.
             * Now using the enhanced obfuscatedXor function instead of simple XOR.
             */
            for (unsigned int i = 0; i < N; i++) {
                m_data[i] = obfuscatedXor(data[i], KEY);
            }
        }

        /*
         * deobfoscate decrypts the strings. Implement decryption algorithm here.
         * Since obfuscatedXor should be its own inverse when used with the same key,
         * we use the same function for decryption.
         */
        void deobfoscate(unsigned char* des) const {
            int i = 0;
            do {
                des[i] = obfuscatedXor(m_data[i], KEY);
                i++;
            } while (des[i - 1]);
        }
    };

    /*
     * This macro is a lambda function to pack all required steps into one single command
     * when defining strings.
     */
#define STR(str) \
    []() -> char* { \
        constexpr auto size = sizeof(str)/sizeof(str[0]); \
        constexpr auto obfuscated_str = obfuscator<size>(str); \
        static char original_string[size]; \
        obfuscated_str.deobfoscate((unsigned char *)original_string); \
        return original_string; \
    }()

}

#ifdef _MSC_VER
#pragma warning(pop)
#endif

#endif