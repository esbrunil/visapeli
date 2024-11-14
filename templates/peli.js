let url = window.location.pathname;
let a = url.slice(0, url.lastIndexOf("/"));
let path = a.slice(0, a.lastIndexOf("/"));

const { BrowserRouter, Routes, Route, Navigate, Link, useParams } = ReactRouterDOM;

const Kysymys = ({userId, kysymys}) => {
  const [question, setQuestion] = React.useState(null);
  const [vaihtoehdot, setKysymys] = React.useState(null);
  const [kysymysIndex, setKysymysIndex] = React.useState(0);
  const [kysymykset, setKysymykset] = React.useState(kysymys.kysymykset);
  const [painettu, setPainettu] = React.useState(false);
  const [aktiivinen, setAktiivinen] = React.useState(-1);
  const [isCorrect, setIsCorrect] = React.useState(null);
  const [aihe, setAihe] = React.useState("Ei asetettu")

  const haeKysymys = async (kysymysIndex) => {
    try {
      const response = await fetch("../haeKysymys", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
          body: JSON.stringify({ kayttajaID: userId.toString(), kysymysID: kysymykset[kysymysIndex].toString() , aihe: kysymys.aiheData.aihe}), });
        if (!response.ok) {
          throw new Error("Virhe");
        }
        const result = await response.json();
        setAihe(kysymys.aiheData.aihe);
        setQuestion(result);
      } catch (error) {
        //
      }
    };

    React.useEffect(() => {
    console.log(kysymykset);
    if (kysymysIndex < kysymykset.length) {
      haeKysymys(kysymysIndex);
      
    }
    else {
      window.location.href = path + "/ValitseAihe";
    }
  }, [kysymysIndex]);

  const tarkistaVastaus = async (vastausId) => {
    try {
      const response = await fetch("../tarkistaVastaus", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          kayttajaID: userId.toString(),
          kysymysID: kysymykset[kysymysIndex].toString(),
          vastaus: vastausId.toString(),
        }),
      });
      if (!response.ok) {
        throw new Error("Virhe tarkistuksessa");
        return true;
      }
      const result = await response.json();
      return true; 
      //return result;
    } catch (error) {
      console.log(error);
    }
  };

  const timeout = "";

  let handleRootClick = () => {
      clearTimeout(timeout);
      seuraavaKysymys();
  }

  let handleAnswerClick = async (e, key, index) => {
    if (painettu) {
      return;
    }
    console.log(index);
    setIsCorrect(null);
    setPainettu(true);
    setAktiivinen(index);

    e.target.className = "painettu vastaus";
    const oikeinko = await tarkistaVastaus(key);

    setIsCorrect(oikeinko);

    const timeout = setTimeout(seuraavaKysymys, 5000);

    let root = document.getElementById("root");

    root.addEventListener("click", handleRootClick);
  };

  let seuraavaKysymys = () => {
      document.getElementById("root").removeEventListener("click", handleRootClick);
      let uusiIndex = kysymysIndex+1
      setKysymysIndex(uusiIndex);
      setPainettu(false);
      setAktiivinen(-1);
  };

  let Kello = () => {
    return (
     <div className="clock">
      <div className="pie spinner"></div>
      <div className="pie paint"></div>
      <div className="mask"></div>
     </div>
    );
  }

  let kysymysJaNapit = (question) => {
    return (
    <div className="kysymysDiv">
        <div className="tiedot">
          
          <div className="kelloDiv"><Kello/></div> 
          <div>{aihe}</div> 
        </div>
        <div className="ylapalkki">
          <h1 className={"kysymys"}>{question.kysymys}</h1>
        </div>
      {Object.entries(question.vastausvaihtoehdot).map(([key, vastaus], index) => (
      <div 
        key={key} 
        className={(aktiivinen === index && isCorrect !== null) 
        ? (isCorrect ? "oikein vastaus" : "vaarin vastaus") 
        : "vastaus"}
        onClick={(e) => handleAnswerClick(e, key, index)}
      >
      {vastaus}
      </div>
  ))}
      {painettu && isCorrect !== null && (
         <p>{isCorrect ? "Oikea vastaus" : "Väärä vastaus"}</p>
      )}
    </div>
    );
  };

  return (
    <div>
      {question && (
        <div className="kysymysJaNapit">
          {kysymysJaNapit(question)}
        </div>
      )}
    </div>
  );
};


const Peli = () => {
  let url = window.location.pathname;
  let pelinAihe = url.slice(url.lastIndexOf("/")+1);

  const [userId, setUserId] = React.useState("");
  const [kysymys, setKysymys] = React.useState();

  React.useEffect(() => {

    const haeId = async () => {
      try {
        const response = await fetch("../annaID"); 
        if (!response.ok) {
          throw new Error("Virhe response ei ole ok");
        }
        const result = await response.text();
        console.log(result);
        setUserId(result); 
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
          body: JSON.stringify({ kayttajaID: kayttajaId.toString() , aihe: pelinAihe }),
        });

        if (!response.ok) {
          throw new Error("Virhe");
        }
        const result = await response.json();
        setKysymys(result);

      } catch (error) {
        console.log("virhe ei onnistu");
      }
    };

    haeId();

  }, []);

  return (<div> {userId && kysymys && (<Kysymys userId={userId} kysymys={kysymys} />)} </div>);
};

const App = () => {
  return <Peli />;
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
<App />
);