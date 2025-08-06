import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"

function App() {
  const [items, setItems] = useState(() => {
    const stored = localStorage.getItem("todos")
    return stored ? JSON.parse(stored) : []
  })
  const [text, setText] = useState("")

  useEffect(() => {
    localStorage.setItem("todos", JSON.stringify(items))
  }, [items])

  function addItem(e) {
    e.preventDefault()
    if (!text.trim()) return
    setItems([...items, { id: Date.now(), text, done: false }])
    setText("")
  }

  function toggleItem(id) {
    setItems(items.map(item => item.id === id ? { ...item, done: !item.done } : item))
  }

  function removeItem(id) {
    setItems(items.filter(item => item.id !== id))
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle className="text-xl">Todo List</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={addItem} className="flex gap-2 mb-4">
            <Input value={text} onChange={e => setText(e.target.value)} placeholder="Add a task..." />
            <Button type="submit">Add</Button>
          </form>
          <ul className="space-y-2">
            {items.map(item => (
              <li key={item.id} className="flex items-center justify-between">
                <button
                  type="button"
                  onClick={() => toggleItem(item.id)}
                  className={`flex-1 text-left ${item.done ? "line-through text-muted-foreground" : ""}`}
                >
                  {item.text}
                </button>
                <Button variant="destructive" size="sm" onClick={() => removeItem(item.id)}>
                  Delete
                </Button>
              </li>
            ))}
            {items.length === 0 && (
              <p className="text-sm text-muted-foreground">No tasks yet</p>
            )}
          </ul>
        </CardContent>
      </Card>
    </div>
  )
}

export default App
