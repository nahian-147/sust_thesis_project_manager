var tree_structure = {
    chart: {
        container: "#OrganiseChart6",
        levelSeparation:    40,
        siblingSeparation:  70,
        subTeeSeparation:   70,
        rootOrientation: "WEST",
        nodeAlign: "TOP",
        scrollbar: "None",
        padding: 35,
        // animateOnInit: true,
        node: { HTMLclass: "evolution-tree" },
        connectors: {
            type: "curve",
            style: {
                "arrow-end": ">",
                "stroke-width": 3,
                "stroke-linecap": "round",
                "stroke": "#41f"
            }
        }
    },

    nodeStructure : { pseudo:true, children:[ { text: { name: 'CFZ78524'} },{ pseudo:true, children:[ { text: { name: 'CIZ78533'} },{ pseudo:true, children:[ { text: { name: 'PTZ78456'} },{ pseudo:true, children:[ { text: { name: 'PLZ78507'} },{ pseudo:true, children:[ { text: { name: 'PDZ78471'} },{ pseudo:true, children:[ { text: { name: 'PVZ78483'} },{ pseudo:true, children:[ { text: { name: 'PDZ78471'} },{ text: { name: 'PDZ78489'} } ] } ] } ] } ] } ] } ] } ] }
};