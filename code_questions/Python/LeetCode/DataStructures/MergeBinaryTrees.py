from TreeFunctions import TreeNode, levelOrderTraversal

class MergeTree:

    def mergeTrees(self, root1, root2):
        # Return the other tree if any one of given tree is empty
        if not root1:
            return root2
        elif not root2:
            return root1
        else:
            levelsRoot1, levelsRoot2, levelCounter = [root1], [root2], 0
            root1.val += root2.val
            # If there is no next Level goNotgo will be 0
            goNotgo = 1
            while goNotgo:
                # Lists to temporary store the nodes of next Level
                tempLevelsRoot1, tempLevelsRoot2 = [], []

                for i in range(2**levelCounter):
                    # Merge the nodes
                    #print(len(levelsRoot1), len(levelsRoot2), levelCounter)
                    if levelsRoot1[i] and levelsRoot2[i]:
                        if levelsRoot1[i].left and levelsRoot2[i].left:
                            tempLevelsRoot1.append(levelsRoot1[i].left)
                            tempLevelsRoot2.append(levelsRoot2[i].left)
                            levelsRoot1[i].left.val += levelsRoot2[i].left.val
                        elif not levelsRoot1[i].left and levelsRoot2[i].left:
                            tempLevelsRoot1.append(None)
                            tempLevelsRoot2.append(levelsRoot2[i].left)
                            levelsRoot1[i].left = levelsRoot2[i].left
                        elif not levelsRoot2[i].left and levelsRoot1[i].left:
                            tempLevelsRoot1.append(levelsRoot1[i].left)
                            tempLevelsRoot2.append(None)
                        else:
                            tempLevelsRoot1.append(None)
                            tempLevelsRoot2.append(None)
                    
                        if levelsRoot1[i].right and levelsRoot2[i].right:
                            tempLevelsRoot1.append(levelsRoot1[i].right)
                            tempLevelsRoot2.append(levelsRoot2[i].right)
                            levelsRoot1[i].right.val += levelsRoot2[i].right.val
                        elif not levelsRoot1[i].right and levelsRoot2[i].right:
                            tempLevelsRoot1.append(None)
                            tempLevelsRoot2.append(levelsRoot2[i].right)
                            levelsRoot1[i].right = levelsRoot2[i].right
                        elif not levelsRoot2[i].right and levelsRoot1[i].right:
                            tempLevelsRoot1.append(levelsRoot1[i].right)
                            tempLevelsRoot2.append(None)
                        else:
                            tempLevelsRoot1.append(None)
                            tempLevelsRoot2.append(None)
                        goNotgo = 1
                    else:
                        if not levelsRoot1[i]:
                            tempLevelsRoot1.append(None)
                            tempLevelsRoot1.append(None)
                        if not levelsRoot2[i]:
                            tempLevelsRoot2.append(None)
                            tempLevelsRoot2.append(None)
                        goNotgo = 0
                    
                    # # Add nodes from Next level for Tree1
                    # if levelsRoot1[i] and levelsRoot1[i].left:
                    #     tempLevelsRoot1.append(levelsRoot1[i].left)
                    #     goNotgo = 1
                    # else:
                    #     tempLevelsRoot1.append(None)
                    #     goNotgo = 0
                    # if levelsRoot1[i] and levelsRoot1[i].right:
                    #     tempLevelsRoot1.append(levelsRoot1[i].right)
                    #     goNotgo = 1
                    # else:
                    #     tempLevelsRoot1.append(None)
                    #     goNotgo = 0

                    # # Add nodes from Next level for Tree2
                    # if levelsRoot2[i] and levelsRoot2[i].left:
                    #     tempLevelsRoot2.append(levelsRoot2[i].left)
                    #     goNotgo = 1
                    # else:
                    #     tempLevelsRoot2.append(None)
                    #     goNotgo = 0
                    # if levelsRoot2[i] and levelsRoot2[i].right:
                    #     tempLevelsRoot2.append(levelsRoot2[i].right)
                    #     goNotgo = 1
                    # else:
                    #     tempLevelsRoot2.append(None)
                    #     goNotgo = 0
                
                # Update the levels with next Level Nodes
                levelsRoot1 = tempLevelsRoot1
                levelsRoot2 = tempLevelsRoot2

                # Increament Level
                levelCounter += 1
            
            return root1

    def mergeTrees(self, root1, root2):
        if not root1:
            return root2

        levelNodes = [(root1, root2)]
        while levelNodes:
            tempNode1, tempNode2 = levelNodes.pop()

            if not tempNode1 or not tempNode2:
                continue

            tempNode1.val += tempNode2.val

            if not tempNode1.left:
                tempNode1.left, tempNode2.left = tempNode2.left, tempNode1.left
            if not tempNode1.right:
                tempNode1.right, tempNode2.right = tempNode2.right, tempNode1.right
            
            levelNodes.append((tempNode1.left, tempNode2.left))
            levelNodes.append((tempNode1.right, tempNode2.right))

        return root1


if __name__ == "__main__":
    sol = MergeTree()

    root1 = TreeNode(1)
    root1.left = TreeNode(3)
    root1.right = TreeNode(2)
    root1.left.left = TreeNode(5)

    root2 = TreeNode(2)
    root2.left = TreeNode(1)
    root2.right = TreeNode(3)
    root2.left.right = TreeNode(4)
    root2.right.right = TreeNode(7)

    """
    [1,null,1,null,1,null,1,null,1,null,1,null,1,null,1,null,1,null,1,null,1,2]
    [1,null,1,null,1,null,1,null,1,null,1,2]
    """
    # root1 = TreeNode(1)
    # root1.right = TreeNode(1)
    # root1.right.right = TreeNode(1)
    # root1.right.right.right = TreeNode(1)
    # root1.right.right.right.right = TreeNode(1)
    # root2 = TreeNode(1)
    # root2.right = TreeNode(1)
    # root2.right.right = TreeNode(1)
    

    print(list(levelOrderTraversal(root1))[0])
    print(list(levelOrderTraversal(root2))[0])

    print(list(levelOrderTraversal(sol.mergeTrees(root1, root2)))[0])