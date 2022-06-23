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
import Modal from 'react-bootstrap/Modal'
import Button from "react-bootstrap/esm/Button";

function App() {
  const childRef = useRef();

  const FocusGraph = React.memo(forwardRef((props, ref) => {
    const fgRef = useRef();
    const [dataGrafoAleatorio, setDataGrafoAleatorio] = useState({
      nodes: [],
      links: [],
    });
    const [canRemoveNode, setCanRemoveNode] = useState(false);
    const [canRemoveLink, setCanRemoveLink] = useState(false);
    const [cooldownTicks, setCooldownTicks] = useState(undefined);
    const [grafoId, setGrafoId] = useState(undefined);

    const [tabla, setTabla] = useState([]);
    const [modoGrafico, setModoGrafico] = useState(true);

    const [sourceAddLink, setSourceAddLink] = useState(null);
    const [targetAddLink, setTargetAddLink] = useState(null);
    const [canAddLink1, setCanAddLink1] = useState(null);
    const [canAddLink2, setCanAddLink2] = useState(null);

    const [show, setShow] = useState(false);
    const handleClose = () => setShow(false);

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

        if(canAddLink1){
          setSourceAddLink(node.id);
          setCanAddLink2(true);
          console.log(sourceAddLink);
        }

        if(canAddLink2){
          setTargetAddLink(node.id);
          setCanAddLink1(false);
          setCanAddLink2(false);
        }

      },
      [canAddLink1, canAddLink2, canRemoveNode, dataGrafoAleatorio, sourceAddLink, targetAddLink]
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

      //const bloomPass = new UnrealBloomPass();
      //bloomPass.strength = 1.65;
      //bloomPass.radius = 0.18;
      //bloomPass.threshold = 0.15;
      //fgRef.current.postProcessingComposer().addPass(bloomPass);
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

      GetGrafoPersonalizado() {
        axios
          .post("/grafo/generaraleatorio", null, { params: {grafo: {NombreGrafo:"xd",  NumeroNodos: 3,  NumeroAristas: 4}}})
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
            //setDataGrafoAleatorio(response.data);
            setGrafoId(response.data.GrafoId);
            return response.data;
          })
          .catch((error) => {
            console.log(error);
            return error;
          });
      },

      GetMatrizAdyacencia() {
        axios
          .get(`/matrizadyacencia/${grafoId}`)
          .then((response) => {
            console.log(response.data);
            setTabla(response.data);
            setModoGrafico(false);
            return response.data;
          })
          .catch((error) => {
            console.log(error);
            return error;
          });
      },

      GetModoGrafico() {
        setModoGrafico(true);
      },

      GetQueyranne() {
        axios
          .get("/queyranne/8")
          .then((response) => {
            console.log(response.data);
            return response.data;
          })
          .catch((error) => {
            console.log(error);
            return error;
          });
      },

      GetMssf() {
        axios
          .get("/mssf/8")
          .then((response) => {
            console.log(response.data);
            return response.data;
          })
          .catch((error) => {
            console.log(error);
            return error;
          });
      },

      GetQClustering() {
        axios
          .get(`/q_clustering/${grafoId}`)
          .then((response) => {
            console.log(response.data);
            setDataGrafoAleatorio(response.data);
            return response.data;
          })
          .catch((error) => {
            console.log(error);
            return error;
          });
      },

      GetQClusteringK() {
        axios
          .get(`/q_clusteringK/${grafoId}`)
          .then((response) => {
            console.log(response.data);
            setDataGrafoAleatorio(response.data);
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

      AddLink() {
        setCanAddLink1(true);
      },

      RmLink() {
        setCanRemoveLink(true);
      },

      canDrag() {
        setCooldownTicks(0);
      },

      handleShow() {
        setShow(true);
      },

    }));

    return (
      <div style={{height: "100vh"}}>

      {modoGrafico &&
        <ForceGraph3D
        ref={fgRef}
              graphData={dataGrafoAleatorio}
              nodeLabel="id"
              onNodeClick={handleNodeClick}
              onLinkClick={handleLinkClick}
              linkCurvature="curvature"
              linkCurveRotation="rotation"
              nodeColor={ (node) => {return node.color} }
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
      } 


      {modoGrafico===false &&
        <table>
          {tabla.map((items, index) => {
            return (
              <tr key={index}>
                {items.map((subItems, sIndex) => {
                  return <td> {subItems} </td>;
                })}
              </tr>
            );
          })}
        </table>
      } 
      

      <Modal show={show} onHide={handleClose}>
        <Modal.Header closeButton>
          <Modal.Title>Modal heading</Modal.Title>
        </Modal.Header>
        <Modal.Body>Woohoo, you're reading this text in a modal!</Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            Close
          </Button>
          <Button variant="primary" onClick={handleClose}>
            Save Changes
          </Button>
        </Modal.Footer>
      </Modal>

      </div>
      
    );
  }));


  

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
                  onClick={() => childRef.current.GetGrafoPersonalizado()}
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
                  onClick={() => childRef.current.AddLink()}
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
                  onClick={() => childRef.current.GetQueyranne()}
                >
                  <span>Algoritmo de Queyranne</span>
                </Dropdown.Item>
                <Dropdown.Item
                  eventKey="2"
                  className="glow-on-hover text-white"
                  onClick={() => childRef.current.GetQClustering()}
                >
                  <span>Algoritmo Q Clustering</span>
                </Dropdown.Item>
                <Dropdown.Item
                  eventKey="2"
                  className="glow-on-hover text-white"
                  onClick={() => childRef.current.GetQClusteringK()}
                >
                  <span>Algoritmo Q Clustering K</span>
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
              <Dropdown.Item 
              href="#" 
              className="glow-on-hover text-white"
              onClick={() => childRef.current.GetModoGrafico()}
              >
                <span>Gráfica</span>
              </Dropdown.Item>
              <Dropdown.Item 
              href="#" 
              className="glow-on-hover text-white"
              onClick={() => childRef.current.GetMatrizAdyacencia()}
              >
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
