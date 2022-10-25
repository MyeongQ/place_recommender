import React, { useState } from 'react';
import Map from './component/Map';
import PersistentDrawerLeft from './component/PersistentDrawer';

export default function App() {
  const [markerPositions, setMarkerPositions] = useState([]);
  const [mapSize, setMapSize] = useState([100, 100]);
  const [login, setLogin] = useState(false);
  const [searchResult, setSearchResult] = React.useState([]);
  
  const markerPositions1 = [
    [33.452278, 126.567803],
    [33.452671, 126.574792],
    [33.451744, 126.572441]
  ];
  const markerPositions2 = [
    [37.499590490909185, 127.0263723554437],
    [37.499427948430814, 127.02794423197847],
    [37.498553760499505, 127.02882598822454],
    [37.497625593121384, 127.02935713582038],
    [37.49629291770947, 127.02587362608637],
    [37.49754540521486, 127.02546694890695],
    [37.49646391248451, 127.02675574250912]
  ];
  
  

  return (
    <React.Fragment>
      <PersistentDrawerLeft onSearch={setSearchResult}/>
      <section>
        <button onClick={() => setMapSize([0, 0])}>Hide</button>
        <button onClick={() => setMapSize([30, 30])}>Resize`${mapSize}`</button>
        <button onClick={() => setMapSize([100, 100])}>Resize (400x400)</button>
      </section>
      <section>
        <button onClick={() => setMarkerPositions(markerPositions1)}>
          Marker Set 1
        </button>
        <button onClick={() => setMarkerPositions(markerPositions2)}>
          Marker Set 2
        </button>
        <button onClick={() => setMarkerPositions([])}>
          Marker Set 3 (empty)
        </button>
      </section>
      <Map markerPositions={markerPositions} size={mapSize} />
    </React.Fragment>
    
    
  );
}