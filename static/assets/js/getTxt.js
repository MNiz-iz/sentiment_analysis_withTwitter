fetch(`${window.origin}/result`, {
  method: "POST",
  credentials: "include",
  body: JSON.stringify(keywoed),
  cache: "no-cache",
  headers: new Headers({
    "content-type": "application/json"
  })
})