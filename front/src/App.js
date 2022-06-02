import "./App.css";
import { ForceGraph3D } from "react-force-graph";
import SpriteText from "three-spritetext";
import { UnrealBloomPass } from "three/examples/jsm/postprocessing/UnrealBloomPass";
import React from "react";
import {
  useRef,
  useCallback,
  useEffect,
  useState,
  forwardRef,
  useImperativeHandle,
} from "react";
import axios from "axios";
import Navbar from "react-bootstrap/Navbar";
import Dropdown from "react-bootstrap/Dropdown";
import DropdownButton from "react-bootstrap/DropdownButton";
import Container from "react-bootstrap/Container";
import ButtonGroup from "react-bootstrap/ButtonGroup";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  const childRef = useRef();

  let myData = {
    nodes: [
      {
        id: 1,
        name: "name1",
        val: 10,
      },
      {
        id: 2,
        name: "name2",
        val: 15,
      },
      {
        id: 3,
        name: "name3",
        val: 10,
      },
    ],
    links: [
      {
        source: 1,
        target: 2,
        weight: 200,
      },
      {
        source: 1,
        target: 1,
        curvature: 1,
        rotation: 0,
        weight: 100,
      },
      {
        source: 3,
        target: 1,
        weight: 100,
      },
      {
        source: 1,
        target: 3,
        weight: 100,
      },
    ],
  };

  const gData = {
    nodes: [...Array(14).keys()].map((i) => ({ id: i })),
    links: [
      { source: 0, target: 1, curvature: 0, rotation: 0, id: 23 },
      { source: 0, target: 1, curvature: 0.8, rotation: 0 },
      { source: 0, target: 1, curvature: 0.8, rotation: (Math.PI * 1) / 6 },
      { source: 0, target: 1, curvature: 0.8, rotation: (Math.PI * 2) / 6 },
      { source: 0, target: 1, curvature: 0.8, rotation: (Math.PI * 3) / 6 },
      { source: 0, target: 1, curvature: 0.8, rotation: (Math.PI * 4) / 6 },
      { source: 0, target: 1, curvature: 0.8, rotation: (Math.PI * 5) / 6 },
      { source: 0, target: 1, curvature: 0.8, rotation: Math.PI },
      { source: 0, target: 1, curvature: 0.8, rotation: (Math.PI * 7) / 6 },
      { source: 0, target: 1, curvature: 0.8, rotation: (Math.PI * 8) / 6 },
      { source: 0, target: 1, curvature: 0.8, rotation: (Math.PI * 9) / 6 },
      { source: 0, target: 1, curvature: 0.8, rotation: (Math.PI * 10) / 6 },
      { source: 0, target: 1, curvature: 0.8, rotation: (Math.PI * 11) / 6 },
      { source: 2, target: 3, curvature: 0.4, rotation: 0 },
      { source: 3, target: 2, curvature: 0.4, rotation: Math.PI / 2 },
      { source: 2, target: 3, curvature: 0.4, rotation: Math.PI },
      { source: 3, target: 2, curvature: 0.4, rotation: -Math.PI / 2 },
      { source: 4, target: 4, curvature: 0.3, rotation: 0 },
      { source: 4, target: 4, curvature: 0.3, rotation: (Math.PI * 2) / 3 },
      { source: 4, target: 4, curvature: 0.3, rotation: (Math.PI * 4) / 3 },
      { source: 5, target: 6, curvature: 0, rotation: 0, id: 20 },
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
      { source: 13, target: 13, curvature: 1, rotation: 0 },
    ],
  };

  const FocusGraph = forwardRef((props, ref) => {
    const fgRef = useRef();
    const [dataGrafoAleatorio, setDataGrafoAleatorio] = useState({
      nodes: [],
      links: [],
    });
    const [canRemoveNode, setCanRemoveNode] = useState(false);
    const [canRemoveLink, setCanRemoveLink] = useState(false);
    const [cooldownTicks, setCooldownTicks] = useState(undefined);

    const handleNodeClick = useCallback(
      (node) => {
        //+
        if (canRemoveNode) {
          const { nodes, links } = dataGrafoAleatorio;

          // Remove node on click
          const newLinks = links.filter(
            (l) => l.source !== node && l.target !== node
          ); // Remove links attached to node
          console.log(node);
          console.log(links);
          console.log(newLinks);
          const newNodes = nodes.filter((l) => l !== node);
          console.log(newNodes);

          setDataGrafoAleatorio({ ...dataGrafoAleatorio, nodes: newNodes, links: newLinks });
          setCanRemoveNode(false);
        }
      },
      [canRemoveNode, dataGrafoAleatorio, setDataGrafoAleatorio]
    );

    const handleLinkClick = useCallback(
      (link) => {
        //+
        if (canRemoveLink) {
          const { nodes, links } = dataGrafoAleatorio;

          // Remove link on click
          console.log(links);
          const newLinks = links.filter((l) => l.index !== link.index);
          console.log(newLinks);
          console.log("hola");
          console.log(link.id);

          setDataGrafoAleatorio({ ...dataGrafoAleatorio, nodes: nodes, links: newLinks });
          console.log(dataGrafoAleatorio);
          setCanRemoveLink(false);
        }
      },
      [canRemoveLink, dataGrafoAleatorio, setDataGrafoAleatorio]
    );

    useEffect(() => {
      const fg = fgRef.current;

      //distancia de acuerdo a atributo
      //fg.d3Force('link').distance(link => {return link.weight});

      const bloomPass = new UnrealBloomPass();
      bloomPass.strength = 1.65;
      bloomPass.radius = 0.18;
      bloomPass.threshold = 0.15;
      fgRef.current.postProcessingComposer().addPass(bloomPass);
    }, []);

    /** 
   

    useEffect(() => {
      setInterval(() => {
        GetGrafoAleatorio();
      }, 1000);
    }, []);


  useEffect(() => {
    setInterval(() => {
      // Add a new connected node every second
      setDataGrafoAleatorio(({ nodes, links }) => {
        const id = nodes.length;
        return {
          nodes: [...nodes, { id }],
          links: [...links, { source: id, target: Math.round(Math.random() * (id-1)) }]
        };
      });
    }, 1000);
  }, []);
  */

    useImperativeHandle(ref, () => ({
      GetGrafoAleatorio() {
        axios
          .get("/grafo/generaraleatorio")
          .then((response) => {
            console.log(response.data);
            setDataGrafoAleatorio(response.data);
            //FocusGraph.setDataGrafoAleatorio(response.data);
            return response.data;
          })
          .catch((error) => {
            return error;
          });
      },

      PostGuardarGrafo() {
        axios
          .post("/grafo",dataGrafoAleatorio)
          .then((response) => {
            console.log(response.data);
            return response.data;
          })
          .catch((error) => {
            console.log(error);
            return error;
          });
      },

      AddNode() {
        setDataGrafoAleatorio(({ nodes, links }) => {
          const id = nodes.length;
          return {
            ...dataGrafoAleatorio,
            nodes: [...nodes, { id: id, name: `name${id}`, val: 15 }],
            links: [...links],
          };
        });
      },

      RmNode() {
        setCanRemoveNode(true);
      },

      RmLink() {
        setCanRemoveLink(true);
      },

      canDrag() {
        setCooldownTicks(0);
      },
    }));

    return (
      <ForceGraph3D
        ref={fgRef}
        graphData={dataGrafoAleatorio}
        nodeLabel="id"
        onNodeClick={handleNodeClick}
        onLinkClick={handleLinkClick}
        linkCurvature="curvature"
        linkCurveRotation="rotation"
        nodeAutoColorBy="id"
        linkThreeObjectExtend={true}
        linkThreeObject={(link) => {
          // extend link with text sprite

          let sprite = new SpriteText(`${link.weight}`);
          if (!link.hasOwnProperty("weight")) {
            sprite = new SpriteText("");
          }
          sprite.color = "lightgrey";
          sprite.textHeight = 1.5;

          return sprite;
        }}
        linkPositionUpdate={(sprite, { start, end }) => {
          const middlePos = Object.assign(
            ...["x", "y", "z"].map((c) => ({
              [c]: start[c] + (end[c] - start[c]) / 2, // calc middle point
            }))
          );

          // Position sprite
          Object.assign(sprite.position, middlePos);
        }}
        cooldownTicks={cooldownTicks}
        onNodeDragEnd={() => setCooldownTicks(undefined)}
        linkDirectionalArrowLength={dataGrafoAleatorio.Dirigido === 1 ? 3.5 : 0}
        linkDirectionalArrowRelPos={1}
      />
    );
  });

  return (
    <div className="App">
      <Navbar variant="dark" bg="dark" expand="lg">
        <Container>
          <Dropdown className="d-inline mx-2" autoClose="inside">
            <Dropdown.Toggle
              id="dropdown-autoclose-inside"
              className="glow-on-hover"
            >
              <span>Archivo</span>
            </Dropdown.Toggle>

            <Dropdown.Menu className="bgGray">
              <DropdownButton
                as={ButtonGroup}
                drop={"end"}
                title={"Nuevo grafo"}
                className="w-100 glow-on-hover2"
                autoClose="inside"
                menuVariant="dark"
              >
                <Dropdown.Item
                  eventKey="1"
                  className="glow-on-hover text-white"
                >
                  <span>Personalizado</span>
                </Dropdown.Item>
                <Dropdown.Item
                  eventKey="2"
                  className="glow-on-hover text-white"
                  onClick={() => childRef.current.GetGrafoAleatorio()}
                >
                  <span>Aleatorio</span>
                </Dropdown.Item>
              </DropdownButton>

              <Dropdown.Item href="#" className="glow-on-hover text-white">
                <span>Abrir</span>
              </Dropdown.Item>
              <Dropdown.Item href="#" className="glow-on-hover text-white">
                <span>Cerrar</span>
              </Dropdown.Item>
              <Dropdown.Item  
                className="glow-on-hover text-white"
                onClick={() => childRef.current.PostGuardarGrafo()}
              >
                <span>Guardar</span>
              </Dropdown.Item>
              <Dropdown.Item href="#" className="glow-on-hover text-white">
                <span>Guardar como</span>
              </Dropdown.Item>

              <DropdownButton
                as={ButtonGroup}
                drop={"end"}
                variant="secondary"
                title={"Exportar datos"}
                className="w-100 glow-on-hover2 text-white bgGray"
                autoClose="inside"
                menuVariant="dark"
              >
                <Dropdown.Item eventKey="1" className="glow-on-hover">
                  <span>Excel</span>
                </Dropdown.Item>
                <Dropdown.Item eventKey="2" className="glow-on-hover">
                  <span>Imagen</span>
                </Dropdown.Item>
                <Dropdown.Item eventKey="2" className="glow-on-hover">
                  <span>PDF</span>
                </Dropdown.Item>
              </DropdownButton>

              <Dropdown.Item href="#" className="glow-on-hover text-white">
                <span>Importar datos</span>
              </Dropdown.Item>
              <Dropdown.Item href="#" className="glow-on-hover text-white">
                <span>Inicio</span>
              </Dropdown.Item>
              <Dropdown.Item href="#" className="glow-on-hover text-white">
                <span>Imprimir</span>
              </Dropdown.Item>
            </Dropdown.Menu>
          </Dropdown>

          <Dropdown className="d-inline mx-2" autoClose="inside">
            <Dropdown.Toggle
              id="dropdown-autoclose-inside"
              className="glow-on-hover"
            >
              <span>Editar</span>
            </Dropdown.Toggle>

            <Dropdown.Menu className="bgGray">
              <Dropdown.Item href="#" className="glow-on-hover text-white">
                <span>Deshacer</span>
              </Dropdown.Item>

              <DropdownButton
                as={ButtonGroup}
                drop={"end"}
                title={"Nodo"}
                className="w-100 glow-on-hover2 text-white bgGray"
                autoClose="inside"
                menuVariant="dark"
              >
                <Dropdown.Item
                  eventKey="1"
                  className="glow-on-hover text-white"
                  onClick={() => childRef.current.AddNode()}
                >
                  <span>Agregar</span>
                </Dropdown.Item>
                <Dropdown.Item
                  eventKey="2"
                  className="glow-on-hover text-white"
                >
                  <span>Editar</span>
                </Dropdown.Item>
                <Dropdown.Item
                  eventKey="2"
                  className="glow-on-hover text-white"
                  onClick={() => childRef.current.RmNode()}
                >
                  <span>Eliminar</span>
                </Dropdown.Item>
                <Dropdown.Item
                  eventKey="2"
                  className="glow-on-hover text-white"
                  onClick={() => childRef.current.canDrag()}
                >
                  <span>Mover</span>
                </Dropdown.Item>
              </DropdownButton>

              <DropdownButton
                as={ButtonGroup}
                drop={"end"}
                variant="secondary"
                title={"Arco"}
                className="w-100 glow-on-hover2 text-white bgGray"
                autoClose="inside"
                menuVariant="dark"
              >
                <Dropdown.Item
                  eventKey="1"
                  className="glow-on-hover text-white"
                >
                  <span>Agregar</span>
                </Dropdown.Item>
                <Dropdown.Item
                  eventKey="2"
                  className="glow-on-hover text-white"
                >
                  <span>Editar</span>
                </Dropdown.Item>
                <Dropdown.Item
                  eventKey="2"
                  className="glow-on-hover text-white"
                  onClick={() => childRef.current.RmLink()}
                >
                  <span>Eliminar</span>
                </Dropdown.Item>
              </DropdownButton>
            </Dropdown.Menu>
          </Dropdown>

          <Dropdown className="d-inline mx-2" autoClose="inside">
            <Dropdown.Toggle
              id="dropdown-autoclose-inside"
              className="glow-on-hover"
            >
              <span>Analizar</span>
            </Dropdown.Toggle>

            <Dropdown.Menu className="bgGray">
              <DropdownButton
                as={ButtonGroup}
                drop={"end"}
                variant="secondary"
                title={"Algoritmos"}
                className="w-100 glow-on-hover2 text-white bgGray"
                autoClose="inside"
                menuVariant="dark"
              >
                <Dropdown.Item
                  eventKey="1"
                  className="glow-on-hover text-white"
                >
                  <span>Algoritmo de Queyranne</span>
                </Dropdown.Item>
                <Dropdown.Item
                  eventKey="2"
                  className="glow-on-hover text-white"
                >
                  <span>Algoritmo Mssf</span>
                </Dropdown.Item>
                <Dropdown.Item
                  eventKey="2"
                  className="glow-on-hover text-white"
                >
                  <span>Algoritmo Q Clustering</span>
                </Dropdown.Item>
                <Dropdown.Item
                  eventKey="2"
                  className="glow-on-hover text-white"
                >
                  <span>Algoritmo 4</span>
                </Dropdown.Item>
              </DropdownButton>
            </Dropdown.Menu>
          </Dropdown>

          <Dropdown className="d-inline mx-2" autoClose="inside">
            <Dropdown.Toggle
              id="dropdown-autoclose-inside"
              className="glow-on-hover"
            >
              <span>Herramienta</span>
            </Dropdown.Toggle>

            <Dropdown.Menu className="bgGray">
              <Dropdown.Item href="#" className="glow-on-hover text-white">
                <span>Ejecución</span>
              </Dropdown.Item>
            </Dropdown.Menu>
          </Dropdown>

          <Dropdown className="d-inline mx-2" autoClose="inside">
            <Dropdown.Toggle
              id="dropdown-autoclose-inside"
              className="glow-on-hover"
            >
              <span>Aplicación</span>
            </Dropdown.Toggle>

            <Dropdown.Menu className="bgGray">
              <Dropdown.Item href="#" className="glow-on-hover text-white">
                <span>Aplicación 1</span>
              </Dropdown.Item>
              <Dropdown.Item href="#" className="glow-on-hover text-white">
                <span>Aplicación 2</span>
              </Dropdown.Item>
              <Dropdown.Item href="#" className="glow-on-hover text-white">
                <span>Aplicación 3</span>
              </Dropdown.Item>
              <Dropdown.Item href="#" className="glow-on-hover text-white">
                <span>Aplicación m</span>
              </Dropdown.Item>
            </Dropdown.Menu>
          </Dropdown>

          <Dropdown className="d-inline mx-2" autoClose="inside">
            <Dropdown.Toggle
              id="dropdown-autoclose-inside"
              className="glow-on-hover"
            >
              <span>Ventana</span>
            </Dropdown.Toggle>

            <Dropdown.Menu className="bgGray">
              <Dropdown.Item href="#" className="glow-on-hover text-white">
                <span>Gráfica</span>
              </Dropdown.Item>
              <Dropdown.Item href="#" className="glow-on-hover text-white">
                <span>Tabla</span>
              </Dropdown.Item>
            </Dropdown.Menu>
          </Dropdown>

          <Dropdown className="d-inline mx-2" autoClose="inside">
            <Dropdown.Toggle
              id="dropdown-autoclose-inside"
              className="glow-on-hover"
            >
              <span>Ayuda</span>
            </Dropdown.Toggle>

            <Dropdown.Menu className="bgGray">
              <Dropdown.Item href="#" className="glow-on-hover text-white">
                <span>Ayuda</span>
              </Dropdown.Item>
              <Dropdown.Item href="#" className="glow-on-hover text-white">
                <span>Acerca de Grafos</span>
              </Dropdown.Item>
            </Dropdown.Menu>
          </Dropdown>
        </Container>
      </Navbar>

      <FocusGraph ref={childRef} />
    </div>
  );
}

export default App;
