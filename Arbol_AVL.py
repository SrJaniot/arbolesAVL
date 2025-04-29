import sys 

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1 


def getHeight(node):
    if not node:
        return 0
    return node.height

def getBalance(node):
    if not node:
        return 0
    return getHeight(node.left) - getHeight(node.right)

def updateHeight(node):
    if node:
        node.height = 1 + max(getHeight(node.left), getHeight(node.right))

def rotate_right(y):
    x = y.left
    T2 = x.right

    x.right = y
    y.left = T2

    updateHeight(y)
    updateHeight(x)

    return x

def rotate_left(x):
    y = x.right
    T2 = y.left

    y.left = x
    x.right = T2

    updateHeight(x)
    updateHeight(y)

    return y

class AVLTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        self.root = self._insert_recursive(self.root, value)

    def _insert_recursive(self, node, value):
        if not node:
            return Node(value)

        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        elif value > node.value:
            node.right = self._insert_recursive(node.right, value)
        else:
            return node 
        
        updateHeight(node)
        
        balance = getBalance(node)

        # Caso 1: Rotación a la derecha
        if balance > 1 and value < node.left.value:
            return rotate_right(node) # Se agregó `return` para devolver el nodo actualizado.
        
        
        # Caso 2: Rotación a la izquierda
        if balance < -1 and value > node.right.value:
            return rotate_left(node) # Se agregó `return` para devolver el nodo actualizado.
        
        
        # Caso 3: Rotación izquierda-derecha
        if balance > 1 and value > node.left.value:
            node.left = rotate_left(node.left)
            return rotate_right(node) # Se agregó `return` para devolver el nodo actualizado.
        
        
        # Caso 4: Rotación derecha-izquierda
        if balance < -1 and value < node.right.value:
            node.right = rotate_right(node.right)
            return rotate_left(node) # Se agregó `return` para devolver el nodo actualizado.
        
        
        return node 
    
    def preOrder(self, node):
        if not node:
            return
        print(node.value, end=" ")
        self.preOrder(node.left)
        self.preOrder(node.right)
    
    #funcion para imprimir el balance y la altura de cada nodo
    def printBalances(self, node):
        if not node:
            return
        print(f"Valor: {node.value}, Balance: {getBalance(node)}, Altura: {getHeight(node)}")
        self.printBalances(node.left)
        self.printBalances(node.right)
        
    #funciones para eliminar un nodo
    def delete(self, value):
        self.root = self._delete_recursive(self.root, value)

    def _delete_recursive(self, node, value):
        if not node:
            return node

        # Buscar el nodo a eliminar
        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # Caso 1: Nodo con un solo hijo o sin hijos
            if not node.left:
                return node.right
            elif not node.right:
                return node.left

            # Caso 2: Nodo con dos hijos
            # Obtener el sucesor en orden (el menor en el subárbol derecho)
            temp = self._get_min_value_node(node.right)
            node.value = temp.value
            node.right = self._delete_recursive(node.right, temp.value)

        # Actualizar la altura del nodo actual
        updateHeight(node)

        # Verificar el balance del nodo actual
        balance = getBalance(node)

        # Caso 1: Rotación a la derecha
        if balance > 1 and getBalance(node.left) >= 0:
            return rotate_right(node)

        # Caso 2: Rotación izquierda-derecha
        if balance > 1 and getBalance(node.left) < 0:
            node.left = rotate_left(node.left)
            return rotate_right(node)

        # Caso 3: Rotación a la izquierda
        if balance < -1 and getBalance(node.right) <= 0:
            return rotate_left(node)

        # Caso 4: Rotación derecha-izquierda
        if balance < -1 and getBalance(node.right) > 0:
            node.right = rotate_right(node.right)
            return rotate_left(node)

        return node

    def _get_min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current
    


avl = AVLTree()
values_to_insert = [10, 20, 30, 40, 50, 25]

print("Insertando valores:", values_to_insert)
for val in values_to_insert:
    avl.insert(val)

print("\n--- Después de inserciones ---")
print("Recorrido en preorden del árbol AVL:")
avl.preOrder(avl.root)
print()
print("\n--- Balance y altura de cada nodo ---")
avl.printBalances(avl.root)


# Insertar un nuevo nodo después de las inserciones iniciales
new_value = 35
print(f"\nInsertando un nuevo valor: {new_value}")
avl.insert(new_value)

# Mostrar el estado actualizado del árbol
print("\n--- Después de insertar el nuevo valor ---")
print("Recorrido en preorden del árbol AVL:")
avl.preOrder(avl.root)
print()
print("\n--- Balance y altura de cada nodo ---")
avl.printBalances(avl.root)


# Eliminar un nodo
value_to_delete = 30
print(f"\nEliminando el valor: {value_to_delete}")
avl.delete(value_to_delete)

# Mostrar el estado actualizado del árbol
print("\n--- Después de eliminar el valor ---")
print("Recorrido en preorden del árbol AVL:")
avl.preOrder(avl.root)
print()
print("\n--- Balance y altura de cada nodo ---")
avl.printBalances(avl.root)
