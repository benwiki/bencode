Map titles = {
  "country": {
    "eng": "What is your current state of residence?",
    "ger": "Was ist Ihr aktueller Standort?",
    "hun": "Mi a jelenlegi tartózkodási helye?",
    "ukr": "Ваше місцезнаходження?",
    "pol": "Jaki jest Twój obecny stan zamieszkania?", // Gdzie teraz jesteś?
  },
  "objective": {
    "eng": "What is your purpose?",
    "ger": "Was ist Ihr Ziel?",
    "hun": "Mi az Ön célja?",
    "ukr": "Яка ваша мета?",
    "pol": "Jaki jest Twój cel?",
  }
};

Map objectiveByLang = {
  "eng": {
    "get-help": "To get help and information",
    "give-help": "To provide local help"
  },
  "ger": {
    "get-help": "Hilfe und Information zu bekommen",
    "give-help": "Lokale Hilfe leisten"
  },
  "hun": {
    "get-help": "Segítséget és információt kapni",
    "give-help": "Helyi segítséget nyújtani"
  },
  "ukr": {
    "get-help": "Отримати інформацію й допомогу",
    "give-help": "Отримати локальну допомогу"
  },
  "pol": {
    "get-help": "Aby uzyskać pomoc i informacje",
    "give-help": "Aby zapewnić lokalną pomoc"
  },
};

Map countryByLang = {
  "eng": {
    "germany": "🇩🇪 Germany",
    "austria": "🇦🇹 Austria",
    "switzerland": "🇨🇭 Switzerland",
    "ukraine": "🇺🇦 Ukraine",
    "hungary": "🇭🇺 Hungary",
    "poland": "🇵🇱 Poland",
  },
  "ger": {
    "germany": "🇩🇪 Deutschland",
    "austria": "🇦🇹 Österreich",
    "switzerland": "🇨🇭 Schweiz",
    "ukraine": "🇺🇦 Ukraine",
    "hungary": "🇭🇺 Ungarn",
    "poland": "🇵🇱 Polen",
  },
  "hun": {
    "germany": "🇩🇪 Németország",
    "austria": "🇦🇹 Ausztria",
    "switzerland": "🇨🇭 Svájc",
    "ukraine": "🇺🇦 Ukrajna",
    "hungary": "🇭🇺 Magyarország",
    "poland": "🇵🇱 Lengyelország",
  },
  "ukr": {
    "germany": "🇩🇪 Німеччина",
    "austria": "🇦🇹 Австрія",
    "switzerland": "🇨🇭 Швейцарія",
    "ukraine": "🇺🇦 україни",
    "hungary": "🇭🇺 Угорщина",
    "poland": "🇵🇱 Польща",
  },
  "pol": {
    "germany": "🇩🇪 Niemcy",
    "austria": "🇦🇹 Austria",
    "switzerland": "🇨🇭 Szwajcaria",
    "ukraine": "🇺🇦 Ukraina",
    "hungary": "🇭🇺 Węgry",
    "poland": "🇵🇱 Polska",
  }
};

Map langByLang = {
  "ukr": "🇺🇦 Українська (Ukrainian)",
  "eng": "🇬🇧/🇺🇸 English (English)",
  "ger": "🇩🇪 Deutsch (German)",
  "hun": "🇭🇺 Magyar (Hungarian)",
  "pol": "🇵🇱 Polski (Polish)",
};

Map webpageByCountryAndPurpose = {
  "hungary": {
    "get-help": {
      "default": "https://ukrainehelp.hu/en",
      "hun": "https://ukrainehelp.hu/hu",
      "ukr": "https://ukrainehelp.hu/uk"
    },
    "give-help": {
      "default": "https://voroskereszt.hu/humanitariancrisis/",
      "hun": "https://voroskereszt.hu/humanitariusvalsag/"
    },
  }
};

Map<String, Map<String, String>> categoryByLang = {
  'hun': {
    'emergency': 'Vészhelyzet',
    'medical_aid': 'Egészségügyi ellátás',
    'crossing': 'Határátkelés',
    'transport': 'Utazás',
    'accomodation': 'Lakhatás',
    'children_edu': 'Gyermekek, oktatás',
    'legal_aid': 'Jogi tanácsadás',
    'communication': 'Kommunikáció (wifi, telefon)',
    'food_drink': 'Étel-ital',
    'pet_animal': 'Kisállatok',
    'money': 'Pénz',
    'work': 'Munkalehetőség',
  },
  'eng': {
    'emergency': 'Emergency',
    'medical_aid': 'Medical aid',
    'crossing': 'Crossing the land',
    'transport': 'Transportation',
    'accomodation': 'Accomodation',
    'children_edu': 'Children and education',
    'legal_aid': 'Legal aid',
    'communication': 'Communication (Phone, SIM, WiFi)',
    'food_drink': 'Food and drinks',
    'pet_animal': 'Pets and animals',
    'money': 'Money',
    'work': 'Work',
  },
  'ukr': {
    'emergency': 'Надзвичайна ситуація',
    'medical_aid': 'Медична допомога',
    'crossing': 'Перетинаючи землю',
    'transport': 'Транспорт',
    'accomodation': 'Житло',
    'children_edu': 'Діти і освіта',
    'legal_aid': 'Юридична допомога',
    'communication': 'Зв\'язок (телефон, SIM, WiFi)',
    'food_drink': 'Харчування',
    'pet_animal': 'Домашні тварини',
    'money': 'Грошовi перекази',
    'work': 'Робота',
  },
  'pol': {
    'emergency': 'Nagłe wypadki',
    'medical_aid': 'Pomoc medyczna',
    'crossing': 'Przejście na drugą stronę lądu',
    'transport': 'Transport',
    'accomodation': 'Zakwaterowanie',
    'children_edu': 'Dzieci i edukacja',
    'legal_aid': 'Pomoc prawna',
    'communication': 'Komunikacja (telefon, SIM, WiFi)',
    'food_drink': 'Żywność i napoje',
    'pet_animal': 'Zwierzęta domowe i zwierzęta',
    'money': 'Pieniądze',
    'work': 'Praca',
  },
  'ger': {
    'emergency': 'Notfall',
    'medical_aid': 'Medizinische Hilfe',
    'crossing': 'Das Land durchqueren',
    'transport': 'Transport',
    'accomodation': 'Unterbringung',
    'children_edu': 'Kinder und Bildung',
    'legal_aid': 'Rechtshilfe',
    'communication': 'Kommunikation (Telefon, SIM, WLAN)',
    'food_drink': 'Essen und Getränke',
    'pet_animal': 'Haustiere',
    'money': 'Geld',
    'work': 'Arbeit',
  },
};
