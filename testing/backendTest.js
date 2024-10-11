window.onload = async () => {

    const uId = await (await fetch("../main.cgi/annaID")).text();

    const obj = {
        userID: uId,
        aihe: "aa"
    }

    console.log(await (await fetch("../main.cgi/asetaAihe", {
        method: "POST",
        body: JSON.stringify(obj),
        headers: {
            "Content-Type": "application/json"
        }
    })).json());
}