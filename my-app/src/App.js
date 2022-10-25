import React, { useState } from 'react';
import Map from './component/Map';
import PersistentDrawerLeft from './component/PersistentDrawer';

export default function App() {
  const [markerPositions, setMarkerPositions] = useState([]);
  const [mapSize, setMapSize] = useState([100, 100]);
  const [searchResult, setSearchResult] = React.useState([]);
  
  const markerPositions1 = [
    [35.158533, 129.160889],
    [35.1476, 129.1301],
    [35.1558, 129.0639],
    [35.1546, 129.1318],
    [35.1594, 129.1727],
    [35.1595842338426, 129.169739237274]
  ];
  const markerPositions2 = [
    [35.158533, 129.160889],
    [35.1476, 129.1301],
    [35.1558, 129.0639],
    [35.1546, 129.1318],
    [35.1594, 129.1727],
    [35.1595842338426, 129.169739237274]
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