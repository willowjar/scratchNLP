import Tkinter
from nltk.draw import tree as drawTree
from nltk.draw.util import CanvasFrame


class TreeView:
    def __init__(self, trees, root=None, make_node=None):
        if root is None:
            window = Tkinter.Tk()
        else:
            window = Tkinter.Toplevel(root)

        window.title("Semantic Tree")
        window.geometry("800x600")

        self.cf = CanvasFrame(window)
        self.cf.pack(side='top', expand=1, fill='both')

        buttons = Tkinter.Frame(window)
        buttons.pack(side='bottom', fill='x')

        self.prev = Tkinter.Button(buttons,
                                   text="Prev",
                                       command=self.prev)
        self.prev.pack(side='left')
        self.next = Tkinter.Button(buttons,
                                   text="Next",
                                       command=self.next)
        self.next.pack(side='left')
        self.printps = Tkinter.Button(buttons,
                                      text="Print to Postscript",
                                          command=self.cf.print_to_file)
        self.printps.pack(side='left')
        self.done = Tkinter.Button(buttons,
                                   text="Done",
                                       command=window.destroy)
        self.done.pack(side='left')
        self.label = Tkinter.Label(buttons,
                                   text="Step 1 of %d" % len(trees))
        self.label.pack(side='right')
        self.prev.configure(state='disabled')

        if make_node:
            self.make_node = make_node

        if not len(trees):
            raise "No trees available to draw"

        self.trees = trees
        self.tree = self.trees[0]
        self.pos = 0
        self.showTree()

        if root is None:
            Tkinter.mainloop()

    def prev(self):
        self.pos -= 1
        if self.pos == 0:
            self.prev.configure(state='disabled')
        self.next.configure(state='normal')
        self.update()

    def next(self):
        self.pos += 1
        if self.pos == len(self.trees) - 1:
            self.next.configure(state='disabled')
        self.prev.configure(state='normal')
        self.update()

    def update(self):
        self.cf.destroy_widget(self.treeWidget)
        self.tree = self.trees[self.pos]
        self.showTree()

    def showTree(self):
        self.treeWidget = drawTree.TreeWidget(self.cf.canvas(),
                                              self.tree,
                                              draggable=1,
                                              shapeable=1)
        self.cf.add_widget(self.treeWidget, 0, 0)
        labelStr = "Tree %d of %s" % (self.pos + 1,
                                      len(self.trees))
        self.label.configure(text=labelStr)
