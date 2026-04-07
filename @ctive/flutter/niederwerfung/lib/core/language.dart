enum Language {
  en("en"), // English
  de("de"), // Deutsch (German)
  hu("hu"), // Hungarian
  ;

  const Language(this.code);
  final String code;

  String get name {
    switch (this) {
      case Language.en:
        return 'English';
      case Language.de:
        return 'Deutsch';
      case Language.hu:
        return 'Magyar';
    }
  }

  String get nameWithFlag {
    switch (this) {
      case Language.en:
        return '🇬🇧🇺🇸 English';
      case Language.de:
        return '🇩🇪 Deutsch (German)';
      case Language.hu:
        return '🇭🇺 Magyar (Hungarian)';
    }
  }
}