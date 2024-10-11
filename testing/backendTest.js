window.onload = async () => {

    const uId = await (await fetch("../main.cgi/annaID")).text();

    const obj = {
        kayttajaID: uId,
        aihe: "history"
    }

    resp = await (await fetch("../main.cgi/asetaAihe", {
        method: "POST",
        body: JSON.stringify(obj),
        headers: {
            "Content-Type": "application/json"
        }
    })).json();

    console.log(resp);
    let aihe = resp["aiheData"]["aihe"];
    let kysymykset = resp["kysymykset"];



    const kysymHaku = {
        kayttajaID: uId,
        aihe: aihe,
        kysymysID: kysymykset[0]
    }

    await (await fetch("../main.cgi/haeKysymys", {
        method: "POST",
        body: JSON.stringify(kysymHaku),
        headers: {
            "Content-Type": "application/json"
        }
    }));
}