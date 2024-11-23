let url = window.location.pathname;
let a = url.slice(0, url.lastIndexOf("/"));
let path = a.slice(0, a.lastIndexOf("/"));

const { BrowserRouter, Routes, Route, Navigate, Link, useParams } = ReactRouterDOM;

const LoadingKuvake = () => {
  return (
    <div className="loadingDiv">
      <div className="loading"></div>
    </div>
  );
}

const laskeFonttiKoko = (str, elementWidth, fonttiKoko) => {
  const length = str.length;
  const mult = elementWidth / (fonttiKoko * length);
  let fontSize = fonttiKoko * mult * 2.5;
  if (fontSize > fonttiKoko) fontSize = fonttiKoko;
  console.log("uuusi fottn", fonttiKoko);
  return Math.round(fontSize);
};

const Kysymys = ({ userId, kysymys }) => {
  let url = window.location.pathname;
  let a = url.slice(0, url.lastIndexOf("/"));
  let path = a.slice(0, a.lastIndexOf("/"));
  const [kysymysIndex, setKysymysIndex] = React.useState(0);
  const [question, setQuestion] = React.useState(null);
  const [loading, setLoading] = React.useState(false);


  React.useEffect(() => {
    const haeKysymys = async () => {
      setLoading(true);

      try {
        const response = await fetch("../haeKysymys", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            kayttajaID: userId.toString(),
            kysymysID: kysymys.kysymykset[kysymysIndex].toString(),
          }),
        });

        if (!response.ok) throw new Error("Virhe kysymyksen haussa");

        const result = await response.json();
        setQuestion(result);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

    if (kysymysIndex < kysymys.kysymykset.length - 1) {
      console.log("haetaan uusi", kysymysIndex, kysymys.kysymykset.length);
      haeKysymys();
    } else {
      window.location.href = path + "/ValitseAihe";
    }
  }, [kysymysIndex]);

  const luoSeuraavaKysymys = () => {
    setKysymysIndex((prevIndex) => prevIndex + 1);
  };

  return (
    <div>
      {loading ? (
        <LoadingKuvake />
      ) : question ? (
        <KysymysJaNapit
          question={question}
          aihe={kysymys.aiheData.aihe}
          seuraavaKysymys={luoSeuraavaKysymys}
          kysymysId={kysymys.kysymykset[kysymysIndex].toString()}
          key={kysymys.kysymykset[kysymysIndex].toString()}
        />
      ) : (
        <LoadingKuvake />
      )}
    </div>
  );
};

const KysymysJaNapit = ({ question, aihe, seuraavaKysymys, kysymysId }) => {
  const [aktiivinen, setAktiivinen] = React.useState(false);
  const [isCorrect, setIsCorrect] = React.useState(null);
  const [painettu, setPainettu] = React.useState(false);
  const [start, setStart] = React.useState(false);
  const [pause, setPause] = React.useState(false);
  const [startAika, setStartAika] = React.useState(null);
  const [kutsuSeuraavaKysymys, setKutsuSeuraavaKysymys] = React.useState(false);
  const [sekunnit, setSekunnit] = React.useState(5);

  const muutaFonttiKoko = (elementId) => {
    const elementit = document.querySelectorAll(elementId);
    for (let i of elementit) {
      const leveys = i.offsetWidth;
      const str = i.textContent;
      let koko = laskeFonttiKoko(str, leveys, window.getComputedStyle(i).fontSize);
      i.style.fontSize = `${koko}px`;
    }
  };

  React.useEffect(() => {
    muutaFonttiKoko(".ylapalkki");
    muutaFonttiKoko(".vastaus");
    setStart(true);
    setStartAika(performance.now());

    return () => {
      document.getElementById("root").removeEventListener('click', seuraavaKysymys);
    };
  }, []);

  React.useEffect(() => {
    if (kutsuSeuraavaKysymys) {
      seuraavaKysymys();
    }
  }, [kutsuSeuraavaKysymys]);


  React.useEffect(() => {
    if (start && !pause) {
      const aikaväli = setInterval(() => {
        setSekunnit(prev => {
          if (prev === 1) {
            handleAikaloppui();
            clearInterval(aikaväli);
            return 0;
          }
          return prev - 1;
        });
      }, 1000);

      return () => clearInterval(aikaväli);
    }
  }, [start, pause]);

  const tarkistaVastaus = async (vastausId) => {
    try {
      const response = await fetch("../tarkistaVastaus", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          kysymysID: kysymysId,
          vastausID: vastausId.toString(),
        }),
      });
      if (!response.ok) {
        throw new Error("Virhe tarkistuksessa");
      }
      const result = await response.json();
      return result;
    } catch (error) {
      console.log(error);
    }
  };

  const handleAnswerClick = async (e, key, index) => {
    if (painettu) return;

    setPainettu(true);
    setAktiivinen(index);
    setPause(true);
    e.target.classList.add("painettu");

    const oikeinko = await tarkistaVastaus(key);
    setIsCorrect(oikeinko);

    const loppu = performance.now();
    const kokonaisaika = (loppu - startAika) / 1000;
    console.log("aikaa meni", kokonaisaika, startAika);

    document.getElementById("root").addEventListener('click', () => { setKutsuSeuraavaKysymys("true"); });


    setTimeout(() => {
      setKutsuSeuraavaKysymys("true");
    }, 3000);
  };

  const aikaLoppui = () => {
    setPainettu(true);
    //TODO HAE OIKEA VASTAUA
    // await haeVastauus 
    document.getElementById("root").addEventListener('click', () => { setKutsuSeuraavaKysymys("true"); });
    setTimeout(() => {
      setKutsuSeuraavaKysymys("true");
    }, 3000);
  };

  const handleAikaloppui = () => {
    console.log("Aika loppui");
    aikaLoppui();
  };

  if (!question || !question.kysymys || !question.vastausvaihtoehdot) {
    return <LoadingKuvake />;
  }

  return (
    <div className="kysymysJaNapit">
      <div className="kysymysDiv">
        <div className="tiedot">
          <div className="kello">{sekunnit}</div>
          <div>{aihe}</div>
        </div>
        <div className="ylapalkki">
          <h1 className="kysymys">{question.kysymys}</h1>
        </div>
        {Object.entries(question.vastausvaihtoehdot).map(([key, vastaus], index) => (
          <div
            key={key}
            className={
              aktiivinen === index && isCorrect !== null
                ? isCorrect
                  ? "oikein vastaus"
                  : "vaarin vastaus"
                : "vastaus"
            }
            onClick={(e) => handleAnswerClick(e, key, index)}
          >
            {vastaus}
          </div>
        ))}
      </div>
    </div>
  );
};


const Peli = () => {
  let url = window.location.pathname;
  let pelinAihe = url.slice(url.lastIndexOf("/") + 1);

  const [userId, setUserId] = React.useState("");
  const [kysymys, setKysymys] = React.useState();


  React.useEffect(() => {
    let id = "";
    const haeId = async () => {
      try {
        const response = await fetch("../annaID");
        if (!response.ok) {
          throw new Error("Virhe response ei ole ok");
        }
        const result = await response.text();
        console.log(result);
        await setUserId(result);
        id = result;
        asetaAihe(result);
      } catch (error) {
        console.error(error);
      }
    };


    const asetaAihe = async (kayttajaId) => {
      try {
        console.log(kayttajaId);
        console.log(pelinAihe, "aihe");
        const response = await fetch("../asetaAihe", {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ kayttajaID: kayttajaId.toString(), aihe: pelinAihe }),
        });

        if (!response.ok) {
          throw new Error("Virhe");
        }
        const result = await response.json();
        setKysymys(result);
        console.log(userId);
        const interval = setInterval(async () => {
          console.log("Sending heartbeat...");
          try {
            const response = await fetch("../heartbeat", {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                kayttajaID: id.toString(),
              }),
            });
            console.log(response);

            if (!response.ok) {
              throw new Error("virhe");
            }

          } catch (error) {
            console.log(error);
          }
        }, 5000);



      } catch (error) {
        console.log("virhe ei onnistu");
      }
    };
    haeId();
  }, []);

  return (
    <div>
      {userId && kysymys && (<Kysymys userId={userId} kysymys={kysymys} />)}
    </div>);
};

const App = () => {
  return <Peli />;
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <App />
);
