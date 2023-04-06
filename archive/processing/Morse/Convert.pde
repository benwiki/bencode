int base = 200;
int dot = base,
    dash = base*3,
    space = base*3,
    wordspace = base*7;

char dotdash (int t) {
  if (t <= dot) return '.';
  else return '-';
}

char letter(String s) {
    switch(s) {
        case ".-": return 'A';
        case "-...": return 'B';
        case "-.-.": return 'C';
        case "-..": return 'D';
        case ".": return 'E';
        case "..-.": return 'F';
        case "--.": return 'G';
        case "....": return 'H';
        case "..": return 'I';
        case ".---": return 'J';
        case "-.-": return 'K';
        case ".-..": return 'L';
        case "--": return 'M';
        case "-.": return 'N';
        case "---": return 'O';
        case ".--.": return 'P';
        case "--.-": return 'Q';
        case ".-.": return 'R';
        case "...": return 'S';
        case "-": return 'T';
        case "..-": return 'U';
        case "...-": return 'V';
        case ".--": return 'W';
        case "-..-": return 'X';
        case "-.--": return 'Y';
        case "--..": return 'Z';
        default: return '@';
    }
}
