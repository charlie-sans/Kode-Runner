-- File_name: resonite.lua
-- Project: test
-- Description: a helpful module for resonite containing some useful functions and variables

local resonite = {}

function resonite.add(a, b)
    return a + b
end

function resonite.sub(a, b)
    return a - b
end

function resonite.mul(a, b)
    return a * b
end

function resonite.mod(a, b)
    return a % b
end

function resonite.power(a, b)
    local result = 1
    for i = 1, b do
        result = result * a
    end
    return result
end

function resonite.factorial(a)
    local result = 1
    for i = 1, a do
        result = result * i
    end
    return result
end

function resonite.isPrime(a)
    if a <= 1 then
        return false
    end
    for i = 2, a - 1 do
        if a % i == 0 then
            return false
        end
    end
    return true
end

function resonite.isEven(a)
    return a % 2 == 0
end

function resonite.isOdd(a)
    return a % 2 ~= 0
end

function resonite.isPositive(a)
    return a > 0
end

function resonite.isNegative(a)
    return a < 0
end

function resonite.clear()
    io.write("\27[H\27[2J")
end

function resonite.open(filename)
    resonite.fp = io.open(filename, "r")
end

function resonite.close()
    if resonite.fp then
        resonite.fp:close()
    end
end

function resonite.read()
    if resonite.fp then
        for line in resonite.fp:lines() do
            print(line)
        end
    end
end

function resonite.write(filename, text)
    local file = io.open(filename, "w")
    file:write(text)
    file:close()
end

function resonite.writeLine(filename, text)
    local file = io.open(filename, "a")
    file:write(text .. "\n")
    file:close()
end

function resonite.writeInt(filename, num)
    local file = io.open(filename, "a")
    file:write(tostring(num))
    file:close()
end

function resonite.writeFloat(filename, num)
    local file = io.open(filename, "a")
    file:write(string.format("%f", num))
    file:close()
end

function resonite.writeDouble(filename, num)
    local file = io.open(filename, "a")
    file:write(string.format("%lf", num))
    file:close()
end

function resonite.writeChar(filename, c)
    local file = io.open(filename, "a")
    file:write(c)
    file:close()
end

function resonite.writeBool(filename, b)
    local file = io.open(filename, "a")
    file:write(tostring(b))
    file:close()
end

function resonite.get_request(url)
    os.execute("curl " .. url)
end

function resonite.post_request(url, data)
    os.execute("curl -X POST " .. url .. " -d " .. data)
end

function resonite.put_request(url, data)
    os.execute("curl -X PUT " .. url .. " -d " .. data)
end

function resonite.delete_request(url)
    os.execute("curl -X DELETE " .. url)
end

return resonite
