const { BrowserRouter, Routes, Route, Navigate, Link, useParams } = ReactRouterDOM;
let url = window.location.pathname;
let path = url.slice(0, url.lastIndexOf("/"));
const ValitseAihe = () => {
  const aiheet = ["History", "Geography"];

  const handleClick = (e, aihe) => {
    window.location.href = `${path}/Peli/${aihe}`;
  };

  return (
    <div className="valitseAihe">
      <h2 className="h1">VISAPELI</h2>
      <div className="aiheet">
        {aiheet.map((aihe, index) => (
          <div
            className="aihe"
            key={index}
            onClick={(e) => handleClick(e, aihe)}
          >
            {aihe.toUpperCase()}
          </div>
        ))}
      </div>
    </div>
  );
};

const App = () => {


  return (
    <BrowserRouter>
      <div>
        <Routes>
          <Route path={path + "/ValitseAihe"} element={<ValitseAihe />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <App />
);
