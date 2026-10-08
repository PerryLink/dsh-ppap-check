# dsh-ppap-check — PPAP प्रस्तुति-तत्वों की पूर्णता की जाँच

`dsh-ppap-check` PPAP प्रस्तुति-तत्वों की एक सूची पढ़ता है — पुर्जे का हेडर और प्रत्येक तत्व की एक पंक्ति — और उस सूची से जो यंत्रवत् जाँचा जा सकता है, वह जाँचता है: ग्राहक द्वारा माँगे गए तत्व का प्रस्तुति-रिकॉर्ड दर्ज है या नहीं, प्रस्तुत तत्व की तिथि भरी है या नहीं, नियंत्रित तत्व (डिज़ाइन रिकॉर्ड, FMEA, नियंत्रण योजना, प्रक्रिया प्रवाह, आयामी परिणाम, MSA) का संस्करण भरा है या नहीं, शीट में पुर्जा-क्रमांक और प्रस्तुति-स्तर लिखा है या नहीं, तत्व-क्रमांक अद्वितीय हैं या नहीं, और तत्व-कॉलम में कोई टेम्पलेट प्लेसहोल्डर शेष नहीं है।

## यह किन सवालों का जवाब देता है

| आपका सवाल | इसका जवाब |
|---|---|
| 「是否要求」 कॉलम में तत्व माँगा गया दर्ज है, पर उसका कोई प्रस्तुति-रिकॉर्ड नहीं है — क्या यह दर्ज होता है? | हाँ। `PP-001` उस पंक्ति को दर्ज करता है जिसमें `required` कॉलम «माँगा गया» माने जाने वाले मानों में से कोई एक रखता है (`是`, `Y`, `yes`, `true`, `要求`, `√`) और `submitted` कॉलम खाली है। यह आपकी ही सूची का वही कॉलम पढ़ता है, कोई अंतर्निहित तत्व-सूची नहीं — कौन-से तत्व माँगे जाते हैं यह ग्राहक के बताए स्तर पर निर्भर है — और यह नहीं आँकता कि जो प्रस्तुत हुआ उसकी विषय-वस्तु स्वीकार्य है या नहीं। |
| पंक्ति में प्रस्तुत दर्ज है, पर तिथि का खाना खाली है। और अगर तिथि भरी हो पर ग्राहक की समय-सीमा के बाद पड़े? | `PP-002` उस पंक्ति को दर्ज करता है जिसका `submitted` कॉलम «प्रस्तुत» माने जाने वाले मानों में है (`是`, `Y`, `yes`, `true`, `已提交`, `√`) और `submittedAt` खाना खाली है। यह केवल देखता है कि तिथि का खाना भरा है — तिथि ग्राहक की परियोजना-योजना में तय समय-सीमा के भीतर पड़ती है या नहीं, यह नहीं देखा जाता। |
| नियंत्रण योजना की पंक्ति भरी है पर उसका संस्करण-खाना खाली है — क्या यह दर्ज होगा? और जिन तत्वों में स्वभावतः संस्करण नहीं होता? | `PP-003` केवल उन तत्व-नामों को देखता है जो `conditionPattern` से मेल खाते हैं — डिज़ाइन रिकॉर्ड, अभियांत्रिकी परिवर्तन, DFMEA/PFMEA, नियंत्रण योजना, प्रक्रिया प्रवाह, आयामी परिणाम, मापन-प्रणाली विश्लेषण, नमूने, जाँच-सहायक, PSW, सामग्री रिपोर्ट, प्रारंभिक प्रक्रिया क्षमता — और ऐसी हर मेल खाती पंक्ति दर्ज करता है जिसका `version` खाना खाली है। यह केवल देखता है कि संस्करण भरा है, यह नहीं कि वह सही या नवीनतम है; किसी तत्व में वास्तव में संस्करण न हो तो पैटर्न को सँकरा करें। |
| तत्वों की सारी पंक्तियाँ पूरी लगती हैं, पर औज़ार कहता है कि सूची में पुर्जा-क्रमांक और स्तर नहीं लिखा। हमारे फ़ॉर्म में स्तर हर पंक्ति पर लिखा होता है। | `PP-004` केवल हेडर पढ़ता है: `partNo` और `level` दोनों सामग्री के शीर्ष पर होने चाहिए। यदि आपका फ़ॉर्म स्तर को विवरण-पंक्तियों में रखता है, तो इस नियम के `fields` बदलें या अपनी अलग जाँच लिखें — यह नियम उन मानों को पंक्तियों के भीतर नहीं खोजता। |
| स्तर के खाने में `Level 3` लिखा है, पर `PP-005` इस पर कुछ नहीं कहता। | `PP-005` की `values` सूची खाली आती है, और खाली का अर्थ है विन्यासित नहीं, इसलिए यह चुपचाप पास होने के बजाय `skipped` में स्वयं को दर्ज करता है। ग्राहक के स्तर-लेखन `values` में भरें, तब सूची से बाहर का कोई भी मान दर्ज होगा। फिर भी यह केवल देखता है कि मान आपकी सूची में है — चुना गया स्तर सही है या नहीं यह ग्राहक का निर्णय है — और इसी कारण यह `info` तक सीमित है। |
| हमारी सूची पिछले साल के टेम्पलेट से उतारी गई: एक तत्व-नाम में अब भी 【待填】 लिखा है और दो पंक्तियों में एक ही तत्व-क्रमांक है। | `PP-006` ऐसा तत्व-नाम दर्ज करता है जिसमें अब भी कोई प्लेसहोल्डर है — `【`, `】`, `{{`, `}}`, `XXX`, `xxx`, `待填`, `待补充`, `TBD`, `todo`, यह `terms` सूची आपके टेम्पलेट के अनुसार बदली जा सकती है। `PP-007` `elementNo` में दोहराया गया तत्व-क्रमांक दर्ज करता है, तुलना में खाली जगह नज़रअंदाज़ की जाती है; ऐसा मिलना आम तौर पर या तो दोहरे पंजीकरण का या क्रमांक गलत उतारे जाने का संकेत है, और इनमें से कौन-सा है यह व्यक्ति द्वारा पुष्ट किया जाना चाहिए। |

## यह किन मानकों पर आधारित है

| दस्तावेज़ | संख्यांक | इन्हें उद्धृत करने वाले नियम |
|---|---|---|
| 《生产件批准程序（PPAP）手册》 | AIAG PPAP（现行版次与条号本次未核实） | PP-001, PP-002, PP-003, PP-004, PP-005, PP-006, PP-007 |

**Boundary:** this plugin checks a **PPAP 提交要素清单** for what a checklist can be held to mechanically —
that an element the customer required carries a submission record, that a submitted element carries a date,
that a controlled element (design record, FMEA, control plan, process flow, dimensional results, MSA) carries
a revision, that the sheet names its part number and submission level, that element numbers are unique, and
that no template placeholder survives. It does **not** decide whether PPAP may be approved, whether the level
is right, or whether an element's content satisfies the customer. **The submission level is the customer's to
set, and this plugin ships no level-to-element mapping.**

> ### ⚠️ Read this before trusting a citation in the report
>
> **Every `excerpt` in this plugin's rule pack says, in so many words, that the clause text was not
> obtained.** The method lives in the automotive **AIAG《生产件批准程序（PPAP）手册》** (and the customer
> specific requirements under IATF 16949). The verification pass could not retrieve verbatim clause text, so
> rather than paraphrase a quotation the pack states the gap in the `excerpt` field itself and puts the
> honest reasoning in `note`. Every rule is therefore `warn` or `info`, and a test asserts that no rule
> claims a quotation it does not have. **When the text is in hand, two things must be done: replace each
> `excerpt` with the real clause, and raise `kind` to `direct`.**
>
> **Which elements must be submitted depends on the level the customer specifies** (Level 1–5), so `PP-001`
> reads the **checklist's own 是否要求 column** rather than any built-in list, and `PP-005`'s level vocabulary
> ships **empty** — with no vocabulary configured it reports itself in `skipped` instead of passing quietly.

## Compatibility

| सतह | स्थिति |
|---|---|
| Harness | peer रेंज `>=0.1.2-rc.1 <0.2.0 \|\| >=0.2.0-0 <0.3.0` — `0.2.0-rc.2` और `0.2.1-alpha.1` दोनों को स्वीकार करने के लिए सत्यापित। **`engines.dsh` जानबूझकर घोषित नहीं**: इसका कोई पाठक नहीं और यह किसी होस्ट को अस्वीकार नहीं कर सकता |
| Node | `^22.19.0 || >=24.0.0` |
| प्लेटफ़ॉर्म | सभी (शुद्ध ESM; कोई नेटिव कोड नहीं, कोई नेटवर्क नहीं, कोई मॉडल कॉल नहीं) |
| टूल मोड | `native`, `ptc` और `both` में काम करता है; पूरे फ़ोल्डर के लिए `ptc` चुनें |

## What it does

नियम-सूची, फ़ील्ड और विस्तृत व्यवहार [README.md](README.md#what-it-does) (अंग्रेज़ी मुख्य संस्करण) में हैं। यह प्लगइन केवल उद्धृत धाराओं के सामने शाब्दिक अंतर सूचीबद्ध करता है और हर न चल पाई जाँच को `skipped` में बताता है।

## Install

```sh
dsh plugin --profile <name> add dsh-ppap-check
dsh --profile <name> --dump-config | grep 'dsh-ppap-check'
```

## Configuration

सभी समायोज्य पैरामीटर `src/config.ts` की Schemastery स्कीमा में हैं, इसलिए कोड बदले बिना `cordis.yml` से बदले जा सकते हैं; प्रति-नियम सीमाएँ `rules/` के नियम-पैक में हैं।

| कुंजी | प्रकार | डिफ़ॉल्ट | विवरण |
|---|---|---|---|
| `rulesFile` | string | `rules/ppap-check.yaml` | नियम-पैक का पथ, पैकेज रूट के सापेक्ष |
| `disabledRules` | string[] | `[]` | बंद करने वाले नियम id; प्रत्येक `skipped` में दिखता है |
| `onlyRules` | string[] | `[]` | केवल ये नियम चलाएँ; खाली होने पर सभी नियम चलते हैं |
| `skipNotes` | string | `""` | हर `skipped` कारण के आगे जोड़ी जाने वाली टिप्पणी |
| `timeoutMs` | number | `120000` | उपकरण का सहकारी समय-सीमा बजट |

## Material format

JSON या YAML स्वीकार्य है। पूरा फ़ील्ड उदाहरण [README.md](README.md#material-format) (अंग्रेज़ी मुख्य संस्करण) में है। पढ़ने की परत में फ़ील्ड वैकल्पिक हैं और जाँच इंजन उन्हें सत्यापित करता है, इसलिए आंशिक निर्यात पर क्रैश के बजाय "अनुपस्थित" श्रेणी के निष्कर्ष मिलते हैं।

## Rule sources

नियम-डेटा कोड से अलग है: प्रत्येक नियम में दस्तावेज़, संख्या, स्रोत की अपनी क्रमांकन-प्रणाली के अनुसार धारा, शब्दशः उद्धरण और स्रोत URL होता है। लोडर लागू करता है कि उद्धरण कम से कम आठ अक्षरों का वास्तविक उद्धरण हो, और जिस जाँच का आधार केवल सामान्य सिद्धांत (`kind: derived-from-principle`, अधिकतम `warn`) या स्थानीय नीति (`kind: institutional-configuration`, अधिकतम `info`) हो, उसे कभी `error` घोषित न किया जाए।

सत्यापित सीमाएँ और जान-बूझकर **न** कहे गए निष्कर्ष [README.md](README.md#rule-sources) (अंग्रेज़ी मुख्य संस्करण) और `rules/evidence/` में हैं।

## Troubleshooting

- **प्लगइन इंस्टॉल हो गया पर टूल दिखता नहीं**: जाँचें कि `main` `lib/index.mjs` पर जाता है और `pnpm run build` ने उसे बनाया है।
- **`dsh plugin add` असंगत बताकर मना करता है**: peer range `0.1.x` और `0.2.x` दोनों को कवर करती है; बाहर होने पर स्पष्ट छूट दें: `dsh plugin --profile <name> allow-version <pkg@ver> --dsh-version <runtime> --accept-risk`।
- **कोई नियम नहीं चला**: `skipped` सरणी देखें।
- **`check` में `manifest-peers` विफल दिखता है**: यह `dsh-plugin-dev` की ज्ञात अपस्ट्रीम समस्या है; रनटाइम इंस्टॉल के समय अनुकूलता लागू करता है।
- **समय खिसका हुआ लगता है**: सारी गणना दिए गए स्ट्रिंग पर वॉल-क्लॉक है।

## Development

```sh
pnpm install
pnpm run typecheck
pnpm test
pnpm run build
node ../scripts/sync-shared.mjs dsh-ppap-check
```

अंतिम कमांड `../_shared` का साझा किट `src/shared/` में कॉपी करता है; हर साझा बदलाव के बाद इसे दोबारा चलाएँ।

## License

[Apache License 2.0](LICENSE) © 2026 dsh-ppap-check contributors.
