+++
title = "ZIG Guide"
date = "2024-07-26"
tags = ["zig"]
draft = false
+++

Variaveis são *snake_case* e fuções são *camelCase*

# Assignment

```zig 
(const|var) identifier[: type] = value
```
- `const` - indica que o `identifier` é uma constante que armazena um valor imutável
- `var` - indica que o `identifier` é uma variavel que armazena um valor mutável
- `type` - é uma anotação do tipo do `identifier` que pode ser omitido se o `value` pode ser inferido

```zig
const constant: i32 = 5; // signed 32-bit constant
var variable: u32 = 5000; // unsigned 32-bit variable

// @as performs an explicit type coercion
const inferred_constant = @as(i32, 5);
var inferred_variable = @as(u32, 5000);
```

# Array

Array literals podem ser omitidos com o uso de `_`:

```zig
const a = [5]u8{ 'h', 'e', 'l', 'l', 'o' };
const b = [_]u8{ 'w', 'o', 'r', 'l', 'd' };
```

Para acessar o tamanho do array:
```zig
const array = [_]u8{ 'h', 'e', 'l', 'l', 'o' };
const length = array.len; // 5
```

# For loops

```zig
test "for" {
    //character literals are equivalent to integer literals
    const string = [_]u8{ 'a', 'b', 'c' };

    for (string, 0..) |character, index| {
        _ = character;
        _ = index;
    }

    for (string) |character| {
        _ = character;
    }

    for (string, 0..) |_, index| {
        _ = index;
    }

    for (string) |_| {}
}
```

# Functions

Todos os argumentos de funções são imutáveis.

# Defer
é util para garantir que recursos sejam limpados quando não forem mais necessários (Exatamente o mesmo padrão em golang)
```zig
const expect = @import("std").testing.expect;

test "defer" {
    var x: i16 = 5;
    {
        defer x += 2;
        try expect(x == 5);
    }
    try expect(x == 7);
}
```

# Errors 

There are no exceptions in zig, errors are values.

```zig
const FileOpenError = error{
    AccessDenied,
    OutOfMemory,
    FileNotFound,
};
const expect = @import("std").testing.expect;

const FileOpenError = error{
    AccessDenied,
    OutOfMemory,
    FileNotFound,
};
const AllocationError = error{OutOfMemory};

test "coerce error from a subset to a superset" {
    const err: FileOpenError = AllocationError.OutOfMemory;
    try expect(err == FileOpenError.OutOfMemory);
}
test "error union" {
    const maybe_error: AllocationError!u16 = 10;
    const no_error = maybe_error catch 0;

    try expect(@TypeOf(no_error) == u16);
    try expect(no_error == 10);
}
```

## *errdefer*
é similar ao defer porém somente é executado quando a função retornar com um erro

```zig
var problems: u32 = 98;

fn failFnCounter() error{Oops}!void {
    errdefer problems += 1;
    try failingFunction();
}

test "errdefer" {
    failFnCounter() catch |err| {
        try expect(err == error.Oops);
        try expect(problems == 99);
        return;
    };
}
```

## catch
o catch é usando no exemplo abaixo com a tecnica `payload capturing` seguida de um trecho de codigo. Nesse cenario o código só é executado se 
ocorrer algum erro na `failingFunction`
```zig 
fn failingFunction() error{Oops}!void {
    return error.Oops;
}

test "returning an error" {
    failingFunction() catch |err| {
        try expect(err == error.Oops);
        return;
    };
}
```


# Referência
[https://zig.guide/](https://zig.guide/)
