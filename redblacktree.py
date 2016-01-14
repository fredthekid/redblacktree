from collections import deque


class Node(object):
    def __init__(self, val=None):
        self.red = True
        self.value = val
        self.left = None
        self.right = None
        self.parent = None

    def getColor(self):
        return "RED" if self.red else "BLACK"

    def setColor(self, color):
        if color == 'r' or color == 'red' or color == 'Red' or color == 'RED':
            self.red = True
        else:
            self.red = False

    def setValue(self, val):
        self.value = val


class RedBlackTree(object):
    def __init__(self):
        self.NilNode = Node()
        self.NilNode.setColor('b')
        self.RootNode = self.NilNode
        self.RootNode.setColor('b')
        self.RootNode.left = self.NilNode
        self.RootNode.right = self.NilNode
        self.RootNode.parent = self.NilNode

    def _createNewNode(self, val, color='r'):
        newNode = Node(val=val)
        newNode.setColor(color)
        newNode.left = self.NilNode
        newNode.right = self.NilNode
        newNode.parent = self.NilNode
        return newNode

    # used for insertion
    def _findParentNode(self, new_val, currNode=None):

        if not currNode:
            currNode = self.RootNode
        if currNode.value == new_val:
            return None
        elif currNode.value < new_val:
            if currNode.right == self.NilNode:
                return currNode
            else:
                return self._findParentNode(new_val, currNode=currNode.right)
        else:
            if currNode.left == self.NilNode:
                return currNode
            else:
                return self._findParentNode(new_val, currNode=currNode.left)

    # returns a Node with minimum value in the subtree of the param root
    def _findMinimum(self, root):
        if root == self.NilNode:
            return self.NilNode
        else:
            minLeft = self._findMinimum(root.left)
            minRight = self._findMinimum(root.right)
            retDict = {}
            if minLeft != self.NilNode:
                retDict[minLeft.value] = minLeft
            if minRight != self.NilNode:
                retDict[minRight.value] = minRight
            retDict[root.value] = root
            return retDict[min(retDict)]

    def minimum(self):
        return self._findMinimum(self.RootNode).value

    def printChild(self, val):
        node = self._findNode(self.RootNode,val)
        print "Left Child: " + str(node.left.value) + "      Right Child: " + str(node.right.value)

    def insert(self, new_val):
        newNode = self._createNewNode(new_val)
        # No Nodes in the Tree yet
        if self.RootNode == self.NilNode:
            self.RootNode = newNode
            self.RootNode.setColor('b')

        # Find parent node
        else:
            parentNode = self._findParentNode(new_val)
            if parentNode is None:
                print "Value is already in the Tree"
                return
            elif parentNode.value > new_val:
                newNode.parent = parentNode
                parentNode.left = newNode
            else:
                newNode.parent = parentNode
                parentNode.right = newNode
            self._maintainTreeAfterInsertion(newNode)

    def _findNode(self, node, val):
        if node == self.NilNode:
            return None
        if node.value == val:
            return node
        elif node.value > val:
            return self._findNode(node.left, val)
        else:
            return self._findNode(node.right, val)

    # used for public calls
    def delete(self, del_val):
        self._deleteNode(self._findNode(self.RootNode, del_val))

    def _deleteHelper(self, delNode, delChild):
        if delNode == self.RootNode:
            self.RootNode = delChild
            delChild.parent = self.NilNode
        elif delNode == delNode.parent.left:
            delNode.parent.left = delChild
            delChild.parent = delNode.parent
        else:
            delNode.parent.right = delChild
            delChild.parent = delNode.parent

    def _deleteNode(self, node):
        if node is None:
            print "Value is not in the tree"
            return
        nodeDelete = node
        replaceNode = None
        color = nodeDelete.getColor()
        if nodeDelete.left == self.NilNode and nodeDelete.right == self.NilNode:
            replaceNode = self.NilNode
            self._deleteHelper(nodeDelete, self.NilNode)
        elif nodeDelete.left == self.NilNode:
            replaceNode = nodeDelete.right
            self._deleteHelper(nodeDelete, nodeDelete.right)
        elif nodeDelete.right == self.NilNode:
            replaceNode = nodeDelete.left
            self._deleteHelper(nodeDelete, nodeDelete.left)
        else:
            nodeMinValue = self._findMinimum(nodeDelete.right)
            replaceNode = nodeMinValue.right
            color = nodeMinValue.getColor()
            nodeDelete.value = nodeMinValue.value
            self._deleteHelper(nodeMinValue, nodeMinValue.right)
        if color == "BLACK":
            self._maintainTreeAfterDeletion(replaceNode)

    def _maintainTreeAfterDeletion(self, node):
        trav = node
        while trav != self.RootNode and trav.getColor() == "BLACK":
            # node that got replaced is a left child
            if trav == trav.parent.left:
                sibling = trav.parent.right
                if sibling.getColor() == "RED":
                    sibling.setColor('b')
                    trav.parent.setColor('r')
                    self.leftRotation(trav.parent)
                    sibling = trav.parent
                if sibling.left.getColor() == "BLACK" and sibling.right.getColor() == "BLACK":
                    sibling.setColor('r')
                    trav = trav.parent
                else:
                    if sibling.right.getColor() == "BLACK":
                        sibling.left.setColor('r')
                        sibling.setColor('r')
                        self.rightRotation(sibling)
                        sibling = trav.parent.right
                    sibling.color = trav.parent.setColor
                    trav.parent.setColor('b')
                    sibling.right.setColor('b')
                    self.leftRotation(trav.parent)
                    trav = self.RootNode
            else:
                sibling = trav.parent.left
                if sibling.getColor() == "RED":
                    sibling.setColor('b')
                    trav.parent.setColor('r')
                    self.rightRotation(trav.parent)
                    sibling = trav.parent
                if sibling.left.getColor() == "BLACK" and sibling.right.getColor() == "BLACK":
                    sibling.setColor('r')
                    trav = trav.parent
                else:
                    if sibling.left.getColor() == "BLACK":
                        sibling.right.setColor('r')
                        sibling.setColor('r')
                        self.leftRotation(sibling)
                        sibling = trav.parent.left
                    sibling.color = trav.parent.setColor
                    trav.parent.setColor('b')
                    sibling.left.setColor('b')
                    self.rightRotation(trav.parent)
                    trav = self.RootNode
        trav.setColor('b')

    # pass in parent as parameter
    def leftRotation(self, rotatePNode):
        rightChild = rotatePNode.right
        rotatePNode.right = rightChild.left
        rightChild.parent = rotatePNode.parent
        if rotatePNode.parent == self.NilNode:
            self.RootNode = rightChild
        elif rotatePNode.parent.left == rotatePNode:
            rotatePNode.parent.left = rightChild
        else:
            rotatePNode.parent.right = rightChild
        rotatePNode.parent = rightChild
        rightChild.left = rotatePNode

    # pass in parent as parameter
    def rightRotation(self, rotatePNode):
        leftChild = rotatePNode.left
        rotatePNode.left = leftChild.right
        leftChild.parent = rotatePNode.parent
        if rotatePNode.parent == self.NilNode:
            self.RootNode = leftChild
        elif rotatePNode.parent.left == rotatePNode:
            rotatePNode.parent.left = leftChild
        else:
            rotatePNode.parent.right = leftChild
        rotatePNode.parent = leftChild
        leftChild.right = rotatePNode

    def _maintainTreeAfterInsertion(self, new_node):
        # if parent is black, no changes to the tree are needed
        if new_node.parent.getColor() == "BLACK":
            return
        currNode = new_node
        count = 0
        while currNode.parent.getColor() == "RED":
            print count
            # if current node's parent is a LEFT CHILD of the current node's grandparent
            if currNode.parent == currNode.parent.parent.left:
                uncleNode = currNode.parent.parent.right
                # if uncle is RED (CASE 1)
                if uncleNode.getColor() == "RED":
                    currNode.parent.setColor('b')
                    uncleNode.setColor('b')
                    currNode.parent.parent.setColor('r')
                    # grandparent of currNode might disrupt the red-black-tree structure, so it needs to be checked
                    currNode = currNode.parent.parent

                # if uncle is BLACK
                else:
                    if currNode == currNode.parent.right:
                        currNode = currNode.parent
                        self.leftRotation(currNode)
                    currNode.parent.setColor('b')
                    currNode.parent.parent.setColor('r')
                    self.rightRotation(currNode.parent.parent)

            # if current node's parent is a RIGHT CHILD of the current node's grandparent
            else:
                uncleNode = currNode.parent.parent.left
                if uncleNode.getColor() == "RED":
                    currNode.parent.setColor('b')
                    uncleNode.setColor('b')
                    currNode.parent.parent.setColor('r')
                    currNode = currNode.parent.parent
                else:
                    if currNode == currNode.parent.left:
                        currNode = currNode.parent
                        self.rightRotation(currNode)
                    currNode.parent.setColor('b')
                    currNode.parent.parent.setColor('r')
                    self.leftRotation(currNode.parent.parent)
        count += 1

        self.RootNode.setColor('b')

    def tree_to_array(self):
        node_arr = []
        q = deque()
        q.append(self.RootNode)
        while len(q) != 0:
            curr = q.popleft()
            if curr != self.NilNode:
                node_arr.append(curr.value)
                q.append(curr.left)
                q.append(curr.right)
            else:
                node_arr.append(None)
        check = node_arr.pop()
        while not check:
            check = node_arr.pop()
        node_arr.append(check)
        return node_arr

    def colors_to_array(self):
        node_arr = []
        q = deque()
        q.append(self.RootNode)
        while len(q) != 0:
            curr = q.popleft()
            if curr != self.NilNode:
                node_arr.append(curr.getColor())
                q.append(curr.left)
                q.append(curr.right)
            else:
                node_arr.append(None)
        check = node_arr.pop()
        while not check:
            check = node_arr.pop()
        node_arr.append(check)
        return node_arr
