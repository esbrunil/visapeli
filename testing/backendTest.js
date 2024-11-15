
let uId;


window.onload = async () => {


    // Requesti "annaID"
    const uId = await (await fetch("../main.cgi/annaID")).text();

        // Lähetetään heartbeat joka 3. sekunti
        setInterval(async () => {
            console.log("interval");
            await heartbeat();
        }, 3000);
    
        // Heartbeat-toteutus
        const heartbeat = async () => {
            const object = {
                kayttajaID: uId
            }
    
            const data = await (await fetch("../main.cgi/heartbeat", {
                method: "POST",
                body: JSON.stringify(object),
                headers: {
                    "Content-Type": "application/json"
                }
            })).text();
        }

    // Tehdään objekti, jossa käyttäjän id ja aiheena hissa
    const obj = {
        kayttajaID: uId,
        aihe: "History"
    }

    // Requesti - asetetaan aiheeksi edellisen objektin aihe
    resp = await (await fetch("../main.cgi/asetaAihe", {
        method: "POST",
        body: JSON.stringify(obj),
        headers: {
            "Content-Type": "application/json"
        }
    })).json();

    // Printataan vastaus, asetetaan aiheeksi vastauksesta saatu aihe ja kysymyksiin lista kysymysten id:istä
    console.log(resp);


    // Olio kysymysten hakuun
    const kysymHaku = {
        kayttajaID: uId,
        kysymysID: resp[0]
    }

    // Requesti kysymyksen hakemiselle annetulla id:llä
    const kyssari = await (await fetch("../main.cgi/haeKysymys", {
        method: "POST",
        body: JSON.stringify(kysymHaku),
        headers: {
            "Content-Type": "application/json"
        }
    }));

    // Testataan vastaus
    const vastausTark = {
        kysymysID: kysymHaku.kysymysID,
        vastausID: 55
    }

    await (await fetch("../main.cgi/tarkistaVastaus", {
        method: "POST",
        body: JSON.stringify(vastausTark),
        headers: {
            "Content-Type": "application/json"
        }
    }));
}