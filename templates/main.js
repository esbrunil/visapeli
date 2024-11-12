let url = window.location.pathname;


let path = url.slice(0, url.lastIndexOf("/"));
const { BrowserRouter, Routes, Route, Navigate, Link, useParams } = ReactRouterDOM;

const ValitseAihe = () => {
  const aiheet = ["history", "geography"];
 
  const handleClick = (aihe) => {
    window.location.href = `${path}/Peli/${aihe}`; 
  };

  return (
    <div className="valitseAihe">
      <h2 className="h1">VISAPELI</h2>
      {aiheet.map((aihe, index) => (
        <div
          className="aihe"
          key={index}
          onClick={() => handleClick(aihe)}
        >
          {aihe.toUpperCase()}
        </div>
      ))}
    </div>
  );
};

const App = () => {
  

return (
  <BrowserRouter>
    <div>
      <Routes>
        <Route path={path + "/ValitseAihe"} element={<ValitseAihe />} />
          <Route path={path + "/"} element={<Navigate to={path + "/ValitseAihe"} replace /> }/>
          <Route path={path} element={<Navigate to={path + "/ValitseAihe"} replace /> }/>
      </Routes>
    </div>
  </BrowserRouter>
);
};

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
<App />
);