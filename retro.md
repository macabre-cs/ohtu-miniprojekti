## Retrospektiivit

### Sprintti 1

Ensimmäisen sprintin retrospektiivi pidettiin heti asiakastapaamisen jälkeen soveltaen [Start, Stop, Continue, More of, Less of  Wheel](https://retrospectivewiki.org/index.php?title=Start,_Stop,_Continue,_More_of,_Less_of_Wheel)
-tekniikkaa. Keskusteltiin tiimin työskentelystä viidestä eri näkökulmasta: mitä uusia toimintatapoja meidän tulisi aloittaa (Start),
mitä voitaisiin lopettaa (Stop), mitä jatketaan (Continue), mitä voitaisiin tehdä lisää (More of) ja mitä voitaisiin tehdä vähemmän (Less of).
Yksi tiimin jäsenistä kirjasi paperille ympyrään ylös lyhyesti oleellisimmat asiat kuhunkin kategoriaan liittyen. Retrospektiivin kesto oli 25 minuuttia.
Alla koottuna keskeiset havainnot sekä kehitystoimenpiteet seuraavaan sprinttiin.

**Start**

Asiat, joita tiimin olisi hyvä aloittaa, liittyivät ensisijaisesti tiimin sisäiseen viestintään ja työnjakoon:
* Sprintin aikana olisi hyvä viestiä muille tiimiläisille, esim. mitä taskeja alkaa tai aikoo tehdä.
* Taskien työnjakoa ei tehty selkeästi heti sprintin alussa. Tästä olisi hyvä sopia ajoissa sprintin aikana, jotta varmistutaan taskien etenemisestä.
* Pariohjelmointia voisi mahdollisuuksien mukaan myös kokeilla.

**Stop**

* Ensimmäisessä sprintissä projektia työstössä käytettiin brancheja, joita nimettiin tekijöiden mukaan. Pohdittiin, että voisi olla selkeämpi käyttää
  ns. feature branceja, jolloin tiedetään paremmin, mitä toiminnallisuuksia missäkin haarassa on kehitetty/kehitetään.

**Continue**

* Todettiin, että yleisesti tiimin työskentely oli ensimmäisessä sprintissä hyvää ja tätä aiotaan jatkaa.

**More of**

* Todettiin, että sprintin jälkeiseen asiakastapaamiseen ja sovelluksen esittelyyn valmistaudutaan paremmin.
* Kommunikointia lisätään ja työskennellessä samaan aikaan voi käyttää myös Discord Voicea.

**Less of**

* Projektin alussa oli luonnollisesti monia käytännön asioita, kuten erilaisten alustojen käyttöönottoa ja ohjeisiin tutustumista, jotka veivät aikaa.
  Näitä asioita tarvitsee tehdä vähemmän seuraavassa sprintissä.

**Kehitystoimenpiteet**

* Jokainen ilmoittaa aktiivisemmin muille tiimiläisille, kun itse alkaa tehdä jotakin sprintin taskeja tai jos on suunnitellut tekevänsä jonkin tietyn taskin.
* Jokainen merkitsee itsensä tekijäksi valitsemiinsa taskeihin projektin kanban-tauluun. Lisäksi taskeihin voi myös laittaa kommentteja, esim. milloin aikoo työstää taskia.
* Versionhallinta: Sovittiin, että nimetään branchit kehitettävän featuren eikä tekijän mukaan. Pieniä muutoksia voi tehdä suoraan main-branchiin pull requestien sijaan.


### Sprintti 2

Sprintin 2 retrospektiivi pidettiin [Glad, Sad, Mad](https://retrospectivewiki.org/index.php?title=Glad,_Sad,_Mad) tekniikalla. Post it lapuille kerättiin sprintin aikana huomattuja positiivisia (glad), negatiivisia (sad) sekä ongelmallisia (mad) asioita, joista keskusteltiin yhdessä. Negatiivisiin ja ongelmallisiin kohtiin pohdittiin myös ratkaisuja/kehityskohteita. Retrospektiivissä kesti noin 20 minuuttia.

**Glad**

* Kommunikaatiota oli enemmän
* Työtä tehtiin tasaisesti
* Uudet branchien nimet olivat hyviä
* Yhteistyö toimi hyvin
* Asiakastapaamiseen valmistauduttiin hyvin

**Sad**
* Merge-vaikeudet
* Kommunikaatio hukkuu discordiin
  * Lisätään kanavia tarpeen vaatiessa
* HTML:n seassa oleva JS tekee templateista epäselviä/hankalia
  * Refaktoroidaan

**Mad**
* Vibe koodausta
  * Yritetään käyttää AI:ta harkitsevammin.
* Trello joskus jäljessä
  * Muistetaan päivittää
* Bugi asiakkaan demossa
  * Selvitetään ja lisätään testi bugia varten


### Sprintti 3

Oli jälleen aika pitää retrospektiivi sprintin jälkeen. Pidimme retron pikaisen ruokatauon jälkeen uuden tekniikan parissa. Tällä kertaa kokeilimme variaatiota [viime viikon tekniikasta](https://retrospectivewiki.org/index.php?title=Glad,_Sad,_Mad), käytimme [Facebook Reactions Retrospective](https://retrospectivewiki.org/index.php?title=Facebook_Reactions_Retrospective)-tekniiikkaa. Retron fasilitoija teki valkotaululle kuusi eri lokeroa, jotka nimettiin Liked, Loved, Made me laugh, Surprised me, Made me sad ja Made me angry. Kaikki ryhmäläiset saivat 7 minuuttia aikaa kirjoittaa havaintoja sprintistä post-it-lapuille, jotka lopuksi laitettiin valkotaululle. Laput käytiin läpi järjestyksessä fasilitoijan johdolla.

**Liked** ja **Loved**

Nämä kaksi kategoriaa tuntuivat olevan liian päällekäisiä, joten niiden yhdistäminen on aiheellista.
* Tiimin kommunikaatio ja henki on hyvää!
* Uudesta muutokset-discord-kanavasta pidettiin kovasti
* Koodi on selkeämpää refaktoroinnin ansiosta
* Projekti etenee ja työnteko on tehokkaampaa
* Vähemmän vaikeuksia mergejen kanssa
* Yksi story jäi kesken, se toimi hyvänä oppimiskokemuksena
* Asiakastapaaminen meni jälleen hyvin

**Made me laugh**
* Asiakastapaamista edeltävä palaveri meni taas yliajalle :D

**Surprised me**
* DOI-tunnisteella viitteen lisäämisen toteuttamisen työläys
* Koodin lukemiseen ja ylläpitoon meni paljon aikaa

**Made me sad**
* Olimme liian optimisia ajan suhteen (esim. taskit veivät enemmän aikaa kuin oletimme)
* Aiempaa haastavat storyt (-> olisiko tarvetta suunnitella tai työskennellä yhdessä enemmän?)
* Oma suoriutuminen ei ollut mitä odotin

**Made me angry**
* Copilot
* Robot Framefork
* Mainin pitäminen ajan tasalla
* Koodaus ei onnistunut kuten olisin toivonut (henkilökohtainen suoriutuminen)

**Kehitystoimenpiteet**

Kun kaikki laput olivat käyty läpi, ryhmälle oli jo rutiininomaisesti syntynyt idea siitä miten voisimme parantaa toimintatapoja seuraavalle sprintille. Valitsimme viimeiselle sprintille storyt, jotka hyvin varmasti saamme toteutettua ongelmitta ajallisesti ja teknisesti. Koimme, että uuden oppimiseen on mennyt joka sprintissä aina enemmän ja enemmän aikaa, joten halusimme nyt keskittyä tuotteen edistämiseen. Sprintissä meni myös paljon aikaa koodin refaktorointiin, joka on eduksemme seuraavassa sprintissä, sillä koodi on luettavampaa. Aiomme tietoisesti ottaa seuraavassa sprintissä teknistä velkaa, jotta saamme tuotteesta mahdollisimman eeppisen loppudemoon. Sovimme myös, että varaamme enemmän aikaa yhteisiin palavereihin, sillä ne ovat venyneet.

**Muita huomioita**

Uuden retrospektiivi-tekniikan kokeilu oli mielekästä, mutta osa kategorioista tuntui vähän turhilta tai päällekäisiltä. Surprised me-kategoria, oli kuitenkin hyvä lisäys ryhmän mielestä. Totesimme, että meille olisi riittänyt kategoriat Glad, Sad, Mad ja Surprised.