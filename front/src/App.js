import logo from './logo.svg';
import './App.css';
import {ForceGraph3D} from 'react-force-graph';
import SpriteText from 'three-spritetext';
import {useRef, useCallback, useEffect} from 'react'


function App() {

  let myData = {
      "nodes": [ 
          { 
            "id": 1,
            "name": "name1",
            "val": 10
          },
          { 
            "id": 2,
            "name": "name2",
            "val": 15
          },
          { 
            "id": 3,
            "name": "name3",
            "val": 10 
          }
      ],
      "links": [
          {
              "source": 1,
              "target": 2,
              "weight": 200
          },
          {
            "source": 1,
            "target": 1,
            "curvature": 1, 
            "rotation": 0,
            "weight": 100 
        } 
      ]
  }
  

  const gData = {
    nodes: [...Array(14).keys()].map(i => ({ id: i })),
    links: [
      { source: 0, target: 1, curvature: 0, rotation: 0 },
      { source: 0, target: 1, curvature: 0.8, rotation: 0 },
      { source: 0, target: 1, curvature: 0.8, rotation: Math.PI * 1 / 6 },
      { source: 0, target: 1, curvature: 0.8, rotation: Math.PI * 2 / 6 },
      { source: 0, target: 1, curvature: 0.8, rotation: Math.PI * 3 / 6 },
      { source: 0, target: 1, curvature: 0.8, rotation: Math.PI * 4 / 6 },
      { source: 0, target: 1, curvature: 0.8, rotation: Math.PI * 5 / 6 },
      { source: 0, target: 1, curvature: 0.8, rotation: Math.PI },
      { source: 0, target: 1, curvature: 0.8, rotation: Math.PI * 7 / 6 },
      { source: 0, target: 1, curvature: 0.8, rotation: Math.PI * 8 / 6 },
      { source: 0, target: 1, curvature: 0.8, rotation: Math.PI * 9 / 6 },
      { source: 0, target: 1, curvature: 0.8, rotation: Math.PI * 10 / 6 },
      { source: 0, target: 1, curvature: 0.8, rotation: Math.PI * 11 / 6 },
      { source: 2, target: 3, curvature: 0.4, rotation: 0 },
      { source: 3, target: 2, curvature: 0.4, rotation: Math.PI / 2 },
      { source: 2, target: 3, curvature: 0.4, rotation: Math.PI },
      { source: 3, target: 2, curvature: 0.4, rotation: -Math.PI / 2 },
      { source: 4, target: 4, curvature: 0.3, rotation: 0 },
      { source: 4, target: 4, curvature: 0.3, rotation: Math.PI * 2 / 3 },
      { source: 4, target: 4, curvature: 0.3, rotation: Math.PI * 4 / 3 },
      { source: 5, target: 6, curvature: 0, rotation: 0 },
      { source: 5, target: 5, curvature: 0.5, rotation: 0 },
      { source: 6, target: 6, curvature: -0.5, rotation: 0 },
      { source: 7, target: 8, curvature: 0.2, rotation: 0 },
      { source: 8, target: 9, curvature: 0.5, rotation: 0 },
      { source: 9, target: 10, curvature: 0.7, rotation: 0 },
      { source: 10, target: 11, curvature: 1, rotation: 0 },
      { source: 11, target: 12, curvature: 2, rotation: 0 },
      { source: 12, target: 7, curvature: 4, rotation: 0 },
      { source: 13, target: 13, curvature: 0.1, rotation: 0 },
      { source: 13, target: 13, curvature: 0.2, rotation: 0 },
      { source: 13, target: 13, curvature: 0.5, rotation: 0 },
      { source: 13, target: 13, curvature: 0.7, rotation: 0 },
      { source: 13, target: 13, curvature: 1, rotation: 0 }
    ]
  };


  const FocusGraph = () => {
    const fgRef = useRef();

    const handleClick = useCallback(node => {
      // Aim at node from outside it
      const distance = 40;
      const distRatio = 1 + distance/Math.hypot(node.x, node.y, node.z);

      fgRef.current.cameraPosition(
        { x: node.x * distRatio, y: node.y * distRatio, z: node.z * distRatio }, // new position
        node, // lookAt ({ x, y, z })
        3000  // ms transition duration
      );
    }, [fgRef]);


    useEffect(() => {
      
      const fg = fgRef.current;

      //distancia de acuerdo a atributo
      //fg.d3Force('link').distance(link => {return link.weight});

    }, []);

    return <ForceGraph3D
      ref={fgRef}
      graphData={myData}
      nodeLabel="id"
      onNodeClick={handleClick}
      linkCurvature="curvature"
      linkCurveRotation="rotation"
      nodeAutoColorBy="id"
      linkThreeObjectExtend={true}
      linkThreeObject={link => {
        // extend link with text sprite
        const sprite = new SpriteText(`${link.weight}`);
        sprite.color = 'lightgrey';
        sprite.textHeight = 1.5;
        return sprite;
      }}
      linkPositionUpdate={(sprite, { start, end }) => {
        const middlePos = Object.assign(...['x', 'y', 'z'].map(c => ({
          [c]: start[c] + (end[c] - start[c]) / 2 // calc middle point
        })));

        // Position sprite
        Object.assign(sprite.position, middlePos);
      }}

    />;
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
      
        <FocusGraph />

    </div>
  );
}

export default App;
