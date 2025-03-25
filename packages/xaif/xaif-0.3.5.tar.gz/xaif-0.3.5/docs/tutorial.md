# xAIF (Extended Argumentation Interchange Format) Documentation

## Overview

xAIF (Extended Argumentation Interchange Format) is an extension of the AIF (Argumentation Interchange Format), designed to handle more flexible and dynamic argument structures in environments of incremental processing. AIF imposes certain constraints, such as requiring relations to have exactly one consequent and at least one antecedent, and limiting interconnections between propositions to relations. While these constraints are valuable in a fully formed argument structure, they can be too restrictive for environments where arguments are being built piecemeal or where intermediate annotations are needed. This is where xAIF comes in. It extends the AIF to allow for both **underspecified** and **overspecified** argumentation structures, making it a more versatile tool for argumentation representation.

### Features of xAIF:
1. **Underspecification**: Some constraints present in basic AIF (such as the number of antecedents or consequents in a relation) are relaxed, allowing for incomplete or evolving argumentation structures.
2. **Overspecification**: Additional structural markup can be added beyond the standard AIF, which can help represent intermediate discourse annotations that go beyond the formal structure of arguments.
3. **JSON-Based**: xAIF is represented in a convenient JSON format, making it easy to handle programmatically and compatible with a wide range of tools and platforms.
4. **Interlingua for Argument Mining**: xAIF serves as the interlingua for the open argument mining framework, facilitating both input and output for all its modules.

## Structure of xAIF

xAIF is represented as a JSON object that contains several key sections. Below is a breakdown of the structure, followed by an example of a sample xAIF representation.

### Main Components:
1. **AIF**: Contains the main argumentation structure, which includes descriptors, edges, locutions, nodes, participants, and scheme fulfillments.
   - **descriptorfulfillments**: Can be used to track how descriptors are fulfilled in the argumentation structure. In basic xAIF, this may be left as `null`.
   - **edges**: Defines the relationships between nodes (propositions or claims), where each edge connects two nodes. Edges are defined with a unique `edgeID` and `fromID` / `toID` indicating the direction of the relation.
   - **locutions**: The utterances associated with participants (e.g., statements or claims made by speakers). Each locution is tied to a node and a participant.
   - **nodes**: Represents individual propositions, claims, or other argumentation elements. Each node is identified by a unique `nodeID`, has associated text (`text`), and a type (`type`), which can specify whether the node is a **Locution (L)**, **Illocution (I)**, **Inference (RA)**, or **Argumentation (YA)**.
   - **participants**: Information about the speakers or contributors to the discourse, identified by a unique `participantID`.
   - **schemefulfillments**: Similar to descriptorfulfillments, but focused on tracking specific argumentation schemes. This can also be `null` in basic implementations.

2. **dialog**: A boolean flag indicating whether the text is part of a dialogue. If set to `true`, the text represents an exchange between two or more participants.
3. **ova**: An array for additional annotations or visualizations that may be required by specific applications.
4. **text**: Contains the raw textual dialogue, with each speaker's contribution marked by their corresponding span IDs, allowing for easy visualization and interaction.

### Example xAIF JSON

```json
{
  "AIF": {
    "descriptorfulfillments": null,
    "edges": [
      {
        "edgeID": 0,
        "fromID": 0,
        "toID": 4
      },
      {
        "edgeID": 1,
        "fromID": 4,
        "toID": 3
      },
      {
        "edgeID": 2,
        "fromID": 1,
        "toID": 6
      },
      {
        "edgeID": 3,
        "fromID": 6,
        "toID": 5
      },
      {
        "edgeID": 4,
        "fromID": 2,
        "toID": 8
      },
      {
        "edgeID": 5,
        "fromID": 8,
        "toID": 7
      },
      {
        "edgeID": 6,
        "fromID": 3,
        "toID": 9
      },
      {
        "edgeID": 7,
        "fromID": 9,
        "toID": 7
      }
    ],
    "locutions": [
      {
        "nodeID": 0,
        "personID": 0
      },
      {
        "nodeID": 1,
        "personID": 1
      },
      {
        "nodeID": 2,
        "personID": 2
      }
    ],
    "nodes": [
      {
        "nodeID": 0,
        "text": "disagreements between party members are entirely to be expected.",
        "type": "L"
      },
      {
        "nodeID": 1,
        "text": "the SNP has disagreements.",
        "type": "L"
      },
      {
        "nodeID": 2,
        "text": "it's not uncommon for there to be disagreements between party members.",
        "type": "L"
      },
      {
        "nodeID": 3,
        "text": "disagreements between party members are entirely to be expected.",
        "type": "I"
      },
      {
        "nodeID": 4,
        "text": "Default Illocuting",
        "type": "YA"
      },
      {
        "nodeID": 5,
        "text": "the SNP has disagreements.",
        "type": "I"
      },
      {
        "nodeID": 6,
        "text": "Default Illocuting",
        "type": "YA"
      },
      {
        "nodeID": 7,
        "text": "it's not uncommon for there to be disagreements between party members.",
        "type": "I"
      },
      {
        "nodeID": 8,
        "text": "Default Illocuting",
        "type": "YA"
      },
      {
        "nodeID": 9,
        "text": "Default Inference",
        "type": "RA"
      }
    ],
    "participants": [
      {
        "firstname": "Speaker",
        "participantID": 0,
        "surname": "1"
      },
      {
        "firstname": "Speaker",
        "participantID": 1,
        "surname": "2"
      }
    ],
    "schemefulfillments": null
  },
  "dialog": true,
  "ova": [],
  "text": {
    "txt": " Speaker 1 <span class=\"highlighted\" id=\"0\">disagreements between party members are entirely to be expected.</span>.<br><br> Speaker 2 <span class=\"highlighted\" id=\"1\">the SNP has disagreements.</span>.<br><br> Speaker 1 <span class=\"highlighted\" id=\"2\">it's not uncommon for there to be disagreements between party members. </span>.<br><br>"
  }
}

## xaif library

`xaif` is a Python library for working with Argument Interchange Format (AIF), primarily designed to facilitate the development, manipulation, and evaluation of argumentat structures. This package provides essential utilities to validate, traverse, and manipulate AIF-compliant JSON structures, enabling users to effectively work with complex argumentation data.

## Features

- Manage argument components: Add and manipulate various components of an argumentation framework, including relations, nodes, and edges.
- Export data in CSV format: Generate tabular representations of argument components with their respective relation types.


## Installation

You can install the `xaif` package via pip:

```sh
pip install xaif
```

## Usage

### Importing the Library

```python
from xaif import AIF
```

### Example

```python
from xaif import AIF

# Sample xAIF JSON 
xaif_data= {
  "AIF": {
    "descriptorfulfillments": null,
    "edges": [
      {
        "edgeID": 0,
        "fromID": 0,
        "toID": 4
      },
      {
        "edgeID": 1,
        "fromID": 4,
        "toID": 3
      },
      {
        "edgeID": 2,
        "fromID": 1,
        "toID": 6
      },
      {
        "edgeID": 3,
        "fromID": 6,
        "toID": 5
      },
      {
        "edgeID": 4,
        "fromID": 2,
        "toID": 8
      },
      {
        "edgeID": 5,
        "fromID": 8,
        "toID": 7
      },
      {
        "edgeID": 6,
        "fromID": 3,
        "toID": 9
      },
      {
        "edgeID": 7,
        "fromID": 9,
        "toID": 7
      }
    ],
    "locutions": [
      {
        "nodeID": 0,
        "personID": 0
      },
      {
        "nodeID": 1,
        "personID": 1
      },
      {
        "nodeID": 2,
        "personID": 2
      }
    ],
    "nodes": [
      {
        "nodeID": 0,
        "text": "disagreements between party members are entirely to be expected.",
        "type": "L"
      },
      {
        "nodeID": 1,
        "text": "the SNP has disagreements.",
        "type": "L"
      },
      {
        "nodeID": 2,
        "text": "it's not uncommon for there to be disagreements between party members.",
        "type": "L"
      },
      {
        "nodeID": 3,
        "text": "disagreements between party members are entirely to be expected.",
        "type": "I"
      },
      {
        "nodeID": 4,
        "text": "Default Illocuting",
        "type": "YA"
      },
      {
        "nodeID": 5,
        "text": "the SNP has disagreements.",
        "type": "I"
      },
      {
        "nodeID": 6,
        "text": "Default Illocuting",
        "type": "YA"
      },
      {
        "nodeID": 7,
        "text": "it's not uncommon for there to be disagreements between party members.",
        "type": "I"
      },
      {
        "nodeID": 8,
        "text": "Default Illocuting",
        "type": "YA"
      },
      {
        "nodeID": 9,
        "text": "Default Inference",
        "type": "RA"
      }
    ],
    "participants": [
      {
        "firstname": "Speaker",
        "participantID": 0,
        "surname": "1"
      },
      {
        "firstname": "Speaker",
        "participantID": 1,
        "surname": "2"
      }
    ],
    "schemefulfillments": null
  },
  "dialog": true,
  "ova": [],
  "text": {
    "txt": " Speaker 1 <span class=\"highlighted\" id=\"0\">disagreements between party members are entirely to be expected.</span>.<br><br> Speaker 2 <span class=\"highlighted\" id=\"1\">the SNP has disagreements.</span>.<br><br> Speaker 1 <span class=\"highlighted\" id=\"2\">it's not uncommon for there to be disagreements between party members. </span>.<br><br>"
  }
}



# Initialize the AIF object with xAIF data (AIF data structure provided as input)
# Here, 'xaif_data' is expected to be a valid xAIF structure in JSON format
aif = AIF(xaif_data)

# Alternatively, initialize the AIF object with raw text data.
# The AIF object will automatically create locutions and other necessary components from the provided text.
aif = AIF("First Sentence.")

# Adding components to the AIF object:

# 1. Adding a new locution (a statement made by a speaker)
# 'component_type' is specified as "locution", and you provide the 'text' of the locution and the 'speaker' name.
# The next available ID (1 in this case) will be automatically assigned to this locution.
aif.add_component(component_type="locution", text="Second Sentence.", speaker="Default Speaker")

# 2. Adding a proposition (a logical statement associated with a locution)
# The 'component_type' is specified as "proposition", and you provide the locution ID (Lnode_ID) and the proposition text.
# The associated locution ID (0) is required. 
# This creates an I-node (proposition node) with the next available ID (2), and a YA (Default Illocuting) node with ID 3.
aif.add_component(component_type="proposition", Lnode_ID=0, proposition="First sentence.")

# 3. Adding another proposition (another logical statement associated with another locution)
# Here, the 'component_type' is again "proposition", and the associated locution ID (1) is required.
# This creates an I-node with ID 4 and a YA-node with ID 5 to anchor the relation between the I-node and the associated locution.
aif.add_component(component_type="proposition", Lnode_ID=1, proposition="Second sentence.")

# 4. Adding an argument relation (representing the logical connection between propositions)
# 'component_type' is specified as "argument_relation", and you provide the relation type (e.g., "RA" for default inference).
# Here, you are creating an argument relation between two I-nodes (IDs 2 and 4), with the relation type "RA".
# This creates an RA node and edges between the I-nodes and the RA-node.
aif.add_component(component_type="argument_relation", relation_type="RA", iNode_ID2=2, iNode_ID1=4)

# Print the generated xAIF structure to visualize the entire argumentation framework
print(aif.xaif)

# Exporting the data:
# To export the argument relations in CSV format, use the get_csv method with "argument-relation" as the argument.
print(aif.get_csv("argument-relation"))  # Exports proposition pairs with argument relations in tabular (CSV) format.

# To export the locution data in CSV format, use the get_csv method with "locution" as the argument.
print(aif.get_csv("locution"))  # Exports locution data in tabular (CSV) format.


```