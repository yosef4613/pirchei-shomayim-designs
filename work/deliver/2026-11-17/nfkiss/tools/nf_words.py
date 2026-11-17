# nfkiss 17.11 — רשימת המילים הרגישות (אנגלית: תת-מחרוזת, בלי תלות באותיות; עברית: מילה עם קידומות) ומשקל לכל אחת. משותף ל-nf_score.py.
EN = {  # word: weight
 'sex':3,'sexy':3,'xxx':3,'porn':4,'p0rn':3,'pr0n':3,'nude':3,'nudity':3,'naked':3,'orgy':4,'erotic':4,'fetish':4,'bdsm':4,'nsfw':3,'milf':4,
 'boob':3,'b00b':3,'tits':3,'titt':3,'pussy':4,'dick':2,'cock':2,'penis':3,'vagina':3,'anal':2,'cum':1,'slut':4,'whore':4,'hooker':3,'escort':2,
 'strip':1,'stripper':3,'lingerie':3,'bikini':3,'thong':3,'kiss':2,'kissing':2,'lust':2,'horny':4,'hentai':4,'xvideo':4,'onlyfans':4,'camgirl':4,
 'gay':1,'lesbian':3,'shemale':4,'fuck':3,'fck':1,'shit':1,'bitch':3,'bastard':2,'damn':1,'nazi':2,'hitler':2,'kkk':1,
 'girl':1,'girls':1,'babe':2,'sexi':3,'hot':0.3,'love':1,'lover':2,'dating':3,'hookup':3,'flirt':3,'romance':2,'wife':1,'bride':1,'wedding':1,
 'bar':0.2,'pub':0.5,'club':0.5,'nightclub':2,'beer':1,'wine':1,'vodka':2,'whisky':2,'whiskey':2,'alcohol':2,'drunk':2,'cocktail':1,
 'casino':2,'poker':2,'gamble':2,'gambling':2,'betting':2,'lottery':1,'roulette':2,'slot':0.3,
 'drug':1,'drugs':2,'weed':2,'cannabis':2,'cocaine':3,'heroin':3,'marijuana':3,
 'swim':0.5,'swimsuit':3,'beach':0.5,'pool':0.3,'spa':0.3,'massage':2,'sauna':1,'bed':0.3,'bedroom':1,'shower':1,'bath':0.3,'body':0.3,
 'dance':0.5,'disco':1,'party':0.5,'model':0.3,'fashion':0.5,'dress':0.5,'woman':0.5,'women':0.5,'lady':0.5,'female':0.5,
 'torrent':2,'proxy':1,'vpn':1,'hack':1,'crack':1,'warez':3,'keygen':3,'cheat':1,
}
HE = {
 'נשיקה':3,'נשיקות':3,'סקס':4,'סקסי':4,'מין':0.5,'ביקיני':3,'עירום':4,'עירומה':4,'ערום':3,'חשפנ':4,'זונה':4,'פורנו':4,'אירוטי':4,'הלבשה תחתונה':3,
 'אהבה':1,'מאוהב':2,'רומנטי':2,'היכרויות':3,'דייט':2,'חתונה':1,'כלה':0.5,'חתן':0.5,'חברה שלי':1,
 'יין':1,'יינות':1,'בירה':1,'וודקה':2,'ויסקי':2,'אלכוהול':2,'שיכור':2,'פאב':1,'בר':0.3,'מועדון':0.5,'דיסקו':1,'מסיבה':0.5,'מסיבות':0.5,
 'קזינו':2,'הימור':2,'הימורים':2,'לוטו':1,'סמים':2,'סם':0.5,
 'בריכה':0.5,'חוף':0.3,'רחצה':0.5,'שחייה':0.5,'בגד ים':2,'בגדי ים':2,'ים':0.1,'מקלחת':1,'מיטה':0.5,'שינה':0.3,'ספא':1,'עיסוי':2,'סאונה':1,
 'בחורה':1,'בחורות':1,'נערה':1,'נערות':1,'אישה':0.3,'נשים':0.3,'גוף':0.3,'דוגמנית':2,'אופנה':0.5,'שמלה':0.5,
 'כנסייה':1,'כנסיה':1,'צלב':1,'חג המולד':1,'נצרות':1,
}
# מילים תמימות שמכילות את המחרוזות (document → cum, space → spa, cockpit → cock …) — לא נספרות (רק אסימון אנגלי שלם שמתאים לאחד מאלה)
import re as _re
BENIGN = _re.compile(r'document|accum|allover|flover|overlap|overl|circum|cucumber|incumb|spa[cwnrtd]|spaw|cockpit|cockatoo|hover|clover|plover|glover|analy|canal|analog|banal|photo|shot|hotel|hotspot|'
 r'shotgun|hotkey|public|publish|sextant|unisex|essex|sexagesimal|title|titan|petit|appetit|competit|partit|repetit|substit|instit|constit|'
 r'pubkey|vpn_|scrap|escape|landscape|strip(?:e|ed|es)|barrel|barrier|bargain|barn|bart|bartender|embark|scumm|cumul|sexp|'
 r'kkk|fck|nsfw|bdsm|milf|tits|titt|boob|b00b|pr0n|p0rn|xxx|cum$')
