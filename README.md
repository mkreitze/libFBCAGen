# Preface

Fashion Based Cellular Automata (FBCA) are self organizing structures that are normal cellular automata with a governing rule set. This rule set allows a single cell of a FBCA to change its state to a nearby more desirable state by evaluating scores assigned to each cell. FBCAs have been found to be extremely useful for level-map genreation in videogames. This comes from an FBCA exhibiting local self organizing behaviour which, when paired with an inital random state, produce level-maps that have similar local behaviour but different overall configurations. 

# put example image here.

# Initalizations
To properly define a FBCA, five parameters are required. As shown in (thesis plug), these parameters are: 
- F -> connectivity of each cell in the FBCA (its neighbourhood)
- g -> the number of updates done to an FBCA before completion 
- n -> number of states in the FBCA 
- S -> the score matrix
- L_0 -> the inital random set of states

For a default FBCA, 
