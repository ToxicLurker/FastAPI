#!/usr/bin/env tarantool

box.cfg{listen = 3301}
-- box.schema.user.passwd('pass')
s = box.schema.space.create('users')
s:format({
         {name = 'id', type = 'string'},
         {name = 'first_name', type = 'string'},
         {name = 'second_name', type = 'string'},
         {name = 'age', type = 'string'},
         {name = 'birthdate', type = 'string', is_nullable=true},
         {name = 'biography', type = 'string', is_nullable=true},
         {name = 'city', type = 'string'},
         {name = 'disabled', type = 'integer'}
         })
-- s:create_index('primary', {
--          type = 'hash',
--          parts = {'id'}
--          })
s:create_index('tindex', {type="TREE", parts={1, 'string'}, unique=true})
s:create_index('secondary', {
         type = 'TREE',
         parts = {'first_name', 'second_name'},
         unique=false
         })

s:insert{'johndoe', 'john', 'doe', '99', '1990-05-01', 'I love cookies', 'Moscow', 0}








-- csv = require("csv")
-- f = require("fio").open("new_people.csv", { "O_RDONLY"})
-- for i, tup in csv.iterate(f) do
-- --     box.space.myspace:insert({tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7]})
--     -- print(tup[1], tup[2], tup[3], tup[4], tup[5], tup[6], tup[7])
--     print(1)
-- end

-- box.space.myspace:create_index('tindex', {type="TREE", parts={1, 'string'}, unique=true})

function myproc(first_name, second_name)
    local tup = s.index.secondary:select({first_name, second_name}) --box.space.users.index.primary:select({id}, {iterator='E'})
    return {tup[1][1], tup[1][2], tup[1][3], tup[1][4], tup[1][5], tup[1][6], tup[1][7], tup[1][8]}
end


function myproc1(first_name, second_name)
    print(s.index.secondary:select({first_name, second_name}))
    local tup = s.index.secondary:select({first_name, second_name}) --box.space.users.index.primary:select({id}, {iterator='E'})
    return {tup[1][1], tup[1][2], tup[1][3], tup[1][4], tup[1][5], tup[1][6], tup[1][7], tup[1][8]}
end

-- id, first_name, second_name, age, birthdate, biography, city, disabled

myproc1('john', 'doe')
print('asdasdsadad')




-- box.cfg{listen = 3301}
-- s = box.schema.space.create('users')
-- s:format({
--          {name = 'id', type = 'string',},
--          {name = 'first_name', type = 'string'},
--          {name = 'second_name', type = 'string'},
--          {name = 'age', type = 'string'},
--          {name = 'birthdate', type = 'string'},
--          {name = 'biography', type = 'string'},
--          {name = 'city', type = 'string'},
--          {name = 'hashed_password', type = 'string'},
--          {name = 'disabled', type = 'integer'}
--          })
-- s:create_index('primary', {
--          type = 'hash',
--          parts = {'id'}
--          })
-- s:insert{'johndoe', 'john', 'doe', nil, '1990-05-01', 'I love cookies', 'Moscow', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 0}
