## References

---

### Docs

- [Google C++ Style Guide](https://google.github.io/styleguide/cppguide.html)
- [Chromium C++ Style Guide](https://github.com/chromium/chromium/blob/master/styleguide/c%2B%2B/c%2B%2B.md)
- [Chromium C++ Dos and Don'ts](https://github.com/chromium/chromium/blob/master/styleguide/c%2B%2B/c%2B%2B-dos-and-donts.md)
- [ISOCpp C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)

### Tools

- [cpplint.py](https://github.com/google/styleguide/blob/gh-pages/cpplint/cpplint.py)
- [clang-format](http://clang.llvm.org/docs/ClangFormat.html)
- [clang-tidy](http://clang.llvm.org/extra/clang-tidy/)

---



## Google Style

---

### Self-contained Headers

``` cpp
// foo.h
void Foo(const std::string& param);
// bar.h
#include <vector>
// baz.cc
#include <string>        // give <string>
#include "foo.h"         // need <string>
#include "bar.h"         // give <vector>
std::vector<int> Bar();  // need <vector>
```

> - [来源](https://google.github.io/styleguide/cppguide.html#Self_contained_Headers)
> - [SF.10: Avoid dependencies on implicitly `#include`d names](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rs-implicit)
>   - 可以通过 `cpplint --filter=+build/include_what_you_use` 检查（然后再手动加上）
> - [SF.11: Header files should be self-contained](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rs-contained)
>   - 可以通过 `foo.cc` 首先引用 `foo.h` 检查（参考：[sec|Names and Order of Includes]）

---

### `#define` Guard

``` cpp
#pragma once            // Bad?

#ifndef FOO_BAR_BAZ_H_  // Good
#define FOO_BAR_BAZ_H_

// file: `foo/bar/baz.h`
// format: <PROJECT>_<PATH>_<FILE>_H_

#endif  // FOO_BAR_BAZ_H_
```

> - [来源](https://google.github.io/styleguide/cppguide.html#The__define_Guard)
> - [SF.8: Use `#include` guards for all `.h` files](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rs-guards)
> - 可以通过 `cpplint --root=PATH` 检查（然后复制出来）
> - 不推荐使用非标准的 `#pragma once`

---

### Forward Declarations

``` cpp
#include "src/foo.h"  // include Foo
class Bar;            // declare Bar
class Baz {
 public:
  Bar* Qux(const Bar&);  // use Bar
 private:
  Foo foo_;              // own Foo
  Bar* bar_ = nullptr;   // refer Bar
};
```

> - [来源](https://google.github.io/styleguide/cppguide.html#Forward_Declarations)
> - [SF.9: Avoid cyclic dependencies among source files](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rs-cycles)
> - 正方观点：节省编译时间，避免重新编译，消除循环依赖（Chromium Style 支持）
> - 反方观点：隐藏依赖关系，可能错误重载基类和派生类参数，不能前向声明嵌套类（Google Style 不支持）
> - 对于值类型的类成员变量，不要为了 前向声明 改用为指针类型（[Chromium Style](https://github.com/chromium/chromium/blob/master/styleguide/c%2B%2B/c%2B%2B.md#forward-declarations-vs-includes)）

---

### Names and Order of Includes

``` cpp
#include "foo/bar/baz.h"  // self
    // blank
#include <stdio.h>        // C
#include <sys/types.h>    // system
    // blank
#include <string>         // C++
    // blank
#include "base/macros.h"  // other libs
#include "foo/bar/qux.h"  // in project
```

> - [来源](https://google.github.io/styleguide/cppguide.html#Names_and_Order_of_Includes)
> - [SF.5: A `.cpp` file must include the `.h` file(s) that defines its interface](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rs-consistency)
>   - 只能编译时检查 函数返回值、类的成员函数 是否匹配
>   - 不能编译时检查 函数参数 是否匹配
>     - 不同参数视为重载，链接时检查
>     - 可利用 名字空间限定符 _(namespace qualifier)_ 在编译时检查（参考：[Use Namespace Qualifiers to Implement Previously Declared Functions](http://llvm.org/docs/CodingStandards.html#use-namespace-qualifiers-to-implement-previously-declared-functions)）
> - 顺序：自身头文件 + 空行 + C/系统头文件 + 空行 + C++ 库 + 空行 + 其他库/当前项目

---

### Namespaces

``` cpp
namespace foo {         // Good
inline namespace bar {  // Bad
using namespace std;    // Bad  in global
                        // Bad? in local
namespace baz = ::baz;  // Bad? in global
                        // Good in local
using std::string;      // Good
}  // namespace bar
}  // namespace foo
```

> - [来源 1](https://google.github.io/styleguide/cppguide.html#Namespaces) / [来源 2](https://google.github.io/styleguide/cppguide.html#Namespace_Formatting)
> - [SF.6: Use `using namespace` directives for transition, for foundation libraries (such as `std`), or within a local scope (only)](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rs-using)（Google Style 不允许）
>   - 反例：TarsCpp [`using namespace std;`](https://github.com/TarsCloud/TarsCpp/blob/v2.1.1/util/include/util/tc_ex.h#L23) 导致 [`namespace promise`](https://github.com/TarsCloud/TarsCpp/blob/711a5ed70c9c70c3cb29ec731d77a3753a489ce5/servant/promise/promise.h#L33) 和 `std::promise` 冲突（[TarsCpp `promise` 已被移除](https://github.com/TarsCloud/TarsCpp/commit/2401420e787aa5fdeeec14621ae34f633ceaefe5#diff-ce8a8875b781dbc3f442408117240665)）
> - [SF.7: Don’t write `using namespace` at global scope in a header file](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rs-using-directive)
> - 不要使用 [`inline namespace`](http://www.stroustrup.com/C++11FAQ.html#inline-namespace)

---

### Unnamed Namespaces and Static

``` cpp
// Good in .cc, Bad in .h
namespace {
constexpr auto kFoo = 42;
void BarImpl() { ... }
}  // namespace

// Good in .cc, Bad in .h
static constexpr auto kFoo = 42;
static void BarImpl() { ... }
```

> - [来源](https://google.github.io/styleguide/cppguide.html#Unnamed_Namespaces_and_Static_Variables)
> - [SF.21: Don’t use an unnamed (anonymous) namespace in a header](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rs-unnamed)
> - [SF.22: Use an unnamed (anonymous) namespace for all internal/nonexported entities](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rs-unnamed2)
> - 也可以使用 `static` 修饰常量/函数

---

### Use of `sizeof`

``` cpp
/* Foo data; */ Bar data;
memset(&data, 0, sizeof(Foo));   // Bad
memset(&data, 0, sizeof(data));  // Good
```

> - [来源](https://google.github.io/styleguide/cppguide.html#sizeof)
> - 如果和变量有关，尽量使用 `sizeof(varname)`，而不是 `sizeof(type)`（因为类型会被修改，但不易察觉）


### Preincrement and Predecrement

``` cpp
for (auto i = ; i != ; i++) {}  // Bad
for (auto i = ; i != ; ++i) {}  // Good
```

> - [来源](https://google.github.io/styleguide/cppguide.html#Preincrement_and_Predecrement)
> - 尽量使用 `++i`/`--i`，避免使用 `i++`/`i--` 生成不需要的临时对象（如果需要，可以使用）

---

### Pointer and Reference Expressions

``` cpp
int x;              // Good
int x, y;           // Good?
int* a;             // Good
int *a;             // Good?
int* a, b;          // Bad, |b| is int
int& m = x;         // Good
int &m = x;         // Good?
int& m = x, n = y;  // Bad, |n| is int
```

> - [来源](https://google.github.io/styleguide/cppguide.html#Pointer_and_Reference_Expressions)
> - [ES.10: Declare one name (only) per declaration](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Res-name-one)（Google Style 没有限制）
> - [NL.18: Use C++-style declarator layout](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rl-ptr)（Google Style 没有限制）

---

### Use of `const`/`constexpr`

``` cpp
class Foo {
 public:
  const Ret* Bar(const Param&) const;
  static constexpr auto kBaz = 42;
};
for (const Foo& foo : arr) {
  const auto qux = ...;  // unnecessary
  const_cast<Foo&>(foo) += qux;  // Bad
}
```

> - [来源 1](http://google.github.io/styleguide/cppguide.html#Use_of_const) / [来源 2](https://google.github.io/styleguide/cppguide.html#Use_of_constexpr)
> - [Con.2: By default, make member functions `const`](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rconst-fct)
>   - 锁、缓存 等数据成员可以使用 `mutable`（逻辑 `const` 即可）
> - [Con.3: By default, pass pointers and references to `const`s](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rconst-ref)
> - [Con.4: Use `const` to define objects with values that do not change after construction](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rconst-const)（Google Style 没有限制）
>   - 在复杂逻辑中，使用 `const` 可以避免错误
>   - 可以使用 lambda 初始化，避免污染（参考：[sec|Lambda for Complex Initialization]）
> - [Con.5: Use `constexpr` for values that can be computed at compile time](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rconst-constexpr)
> - [ES.50: Don’t cast away `const`](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Res-casts-const)

---

### Local Variables

``` cpp
int i;               // Bad
i = f();
std::vector<int> v;  // Bad
v.push_back(1);
v.push_back(2);

int i = f();                  // Good
std::vector<int> v = {1, 2};  // Good
while (auto i = YieldI()) {}  // Good
```

> - [来源](https://google.github.io/styleguide/cppguide.html#Local_Variables)
> - [ES.20: Always initialize an object](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Res-always)
> - [ES.21: Don’t introduce a variable (or constant) before you need to use it](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Res-introduce)
> - [ES.22: Don’t declare a variable until you have a value to initialize it with](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Res-init)
> - 参考：[sec|Names and Scopes]

---

### Constructors

``` cpp
class Foo {
 public:
  void Init(...);         // Bad
  Foo() /* noexcept */ {
    if (...) throw Err;   // Bad?
    this->VirtualFn(); }  // Bad
  static std::unique_ptr<Foo> Create() {
    ret->VirtualFn(); }   // Good
};
```

> - [来源](https://google.github.io/styleguide/cppguide.html#Doing_Work_in_Constructors)
> - [NR.5: Don’t use two-phase initialization](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rnr-two-phase-init)
> - [C.41: A constructor should create a fully initialized object](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rc-complete)
> - 如果 允许异常，[C.42: If a constructor cannot construct a valid object, throw an exception](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rc-throw)（Google Style 不允许）
> - 如果 禁用异常，可以使用 工厂方法 `Create()` 支持构造失败
>   - 建议返回 智能指针（参考：[sec|Smart Pointers Ownership]）保存多态对象（参考：[sec|Polymorphic Classes Slicing]）
>   - 不要同时提供 `public` 构造函数 和 工厂方法（参考：[Don't mix `Create()` factory methods and public constructors in one class](https://github.com/chromium/chromium/blob/master/styleguide/c%2B%2B/blink-c++.md#dont-mix-create-factory-methods-and-public-constructors-in-one-class)）
> - [C.82: Don’t call virtual functions in constructors and destructors](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rc-ctor-virtual)
> - [C.50: Use a factory function if you need “virtual behavior” during initialization](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rc-factory)

---

### Structs vs. Classes

``` cpp
struct Node {
  Node() { depth_ = ...; }  // Bad
  void InvertBinaryTree();  // Bad
  Node* left = nullptr;     // Good
  Node* right = nullptr;    // Good
  void Reset();             // Good?
 private:
  size_t depth_ = 0;        // Bad
};
```

> - [来源](https://google.github.io/styleguide/cppguide.html#Structs_vs._Classes)
> - [C.2: Use `class` if the class has an invariant; use `struct` if the data members can vary independently](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rc-struct)
> - [C.8: Use `class` rather than `struct` if any member is non-public](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rc-class)
> - [C.40: Define a constructor if a class has an invariant](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rc-ctor)

---

### Access Control

``` cpp
class Foo {
 public:
  Bar bar_;                     // Bad
  static constexpr int k = 42;  // Good
 protected:
  Baz baz_;  // has invariant?  // Bad
 private:
  Qux qux_;                     // Good
};
```

> - [来源](https://google.github.io/styleguide/cppguide.html#Access_Control)
> - [C.9: Minimize exposure of members](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rc-private)
> - [C.133: Avoid `protected` data](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rh-protected)

---

### Implicit Conversions

``` cpp
class Foo {
 public:
  Foo(Bar bar);          // Bad
  operator Baz() const;  // Bad

  explicit Foo(Bar bar);          // Good
  explicit operator Baz() const;  // Good
};
```

> - [来源](https://google.github.io/styleguide/cppguide.html#Implicit_Conversions)
> - [C.46: By default, declare single-argument constructors explicit](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rc-explicit)
> - [C.164: Avoid implicit conversion operators](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Ro-conversion)
> - 尤其是 隐式转换 + 异常 容易出错（参考：[sec|Exceptions]）

---

### Copyable Types (Movable)

``` cpp
class Foo {
 public:
  Foo(const Foo&) = default;
  Foo& operator=(const Foo&) = default;

  // move operations implicit deleted:
  Foo(Foo&&) = default;
  Foo& operator=(Foo&&) = default;
};
```

> - [来源](https://google.github.io/styleguide/cppguide.html#Copyable_Movable_Types)
> - 可拷贝（可移动）：可以写 `copy = default;` 和 `move = default;`
> - 最好都不写（[C.20: If you can avoid defining default operations, do](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rc-zero)）

---

### Copyable Types (Not Movable)

``` cpp
class Foo {
 public:
  Foo(const Foo&) = default;
  Foo& operator=(const Foo&) = default;

  // move operations implicit deleted:
  // Foo(Foo&&) = delete;
  // Foo& operator=(Foo&&) = delete;
};
```

> - [来源](https://google.github.io/styleguide/cppguide.html#Copyable_Movable_Types)
> - 可拷贝（不可移动）：只需要写 `copy = default;`，不需要写 `move = delete;`

---

### MoveOnly Types

``` cpp
class Foo {
 public:
  Foo(Foo&&) = default;
  Foo& operator=(Foo&&) = default;

  // copy operations implicit deleted:
  // Foo(const Foo&) = delete;
  // Foo& operator=(const Foo&) = delete;
};
```

> - [来源](https://google.github.io/styleguide/cppguide.html#Copyable_Movable_Types)
> - 仅移动（不可拷贝）：只需要写 `move = default;`，不需要写 `copy = delete;`

---

### Not Copyable Or Movable Types

``` cpp
class Foo {
 public:
  Foo(const Foo&) = delete;
  Foo& operator=(const Foo&) = delete;

  // move operations implicit deleted:
  // Foo(Foo&&) = delete;
  // Foo& operator=(Foo&&) = delete;
};
```

> - [来源](https://google.github.io/styleguide/cppguide.html#Copyable_Movable_Types)
> - 不可拷贝或移动：只需要写 `copy = delete;`，不需要写 `move = delete;`
> - 最好都写（[C.21: If you define or `=delete` any default operation, define or `=delete` them all](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rc-five)）

---

### Declaration Order

``` cpp
class Foo {
 public:
  using Bar = int;  ...  enum { k = 1 };
  static std::unique_ptr<Foo> Create();
  Foo();  ...  Foo(Foo&&);  ...  ~Foo();
  /* inline */ Bar bar() const { ... }
 private:
  void QuxImpl();  ...  Bar bar_;
};
```

> - [来源](https://google.github.io/styleguide/cppguide.html#Declaration_Order)
> - [NL.16: Use a conventional class member declaration order](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rl-order)
> - 顺序：
>   - `public` + `protected` + `private`（空则不写）
>   - 类型（`typedef`/`using`/嵌套类）+ 常量（`constexpr`/`enum`）+ 工厂方法 + 构造函数 + 构造函数（拷贝/移动）+ 赋值函数（拷贝/移动）+ 析构函数 + 成员函数（静态/方法）+ 数据成员（静态/普通）
> - 注意：
>   - 在类定义中，可以内联定义 accessor(getter)、mutator(setter) 和 空函数
>   - 不要定义长函数，不需要显式 `inline`（参考：[Don’t use `inline` when defining a function in a class definition](http://llvm.org/docs/CodingStandards.html#don-t-use-inline-when-defining-a-function-in-a-class-definition)）
>   - 建议在 静态成员（函数/数据）上一行加 `// static` 注释，可在代码折叠后方便查看

---

### Inheritance

``` cpp
class Foo : /* private */ Bar,  // Bad?
            protected BarImpl,  // Bad
            public IBar {       // Good
 public:
  virtual void IFooFn() = 0;    // Good
  int IBarFn(int=42) override;  // Good?
  /* virtual */ int IBarFn();   // Bad
  bool IBarFn(float) override;  // Check
};
```

> - [来源](https://google.github.io/styleguide/cppguide.html#Inheritance)
> - [C.128: Virtual functions should specify exactly one of `virtual`, `override`, or `final`](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rh-override)
> - [C.129: When designing a class hierarchy, distinguish between implementation inheritance and interface inheritance](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rh-kind)
> - [C.135: Use multiple inheritance to represent multiple distinct interfaces](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rh-mi-interface)
> - [C.136: Use multiple inheritance to represent the union of implementation attributes](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rh-mi-implementation)（Google Style 不允许）
> - 编译器无法检查 [C.140: Do not provide different default arguments for a virtual function and an overrider](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rh-virtual-default-arg)
> - 避免使用 `private` 和 `protected` 继承

---

### Parameters and Arguments

``` cpp
MaybeMultiOut fn(  // ISOCpp
      T   in_not_null_mutable,
const T&  in_not_null_const,
      T*  in_nullable_mutable,
const T*  in_nullable_const,
      T&& in_move_or_forward,
      T*  in_out,  // Google
      T&  in_out,  // ISOCpp
      T*  out);    // Google
```

> - [来源 1](https://google.github.io/styleguide/cppguide.html#Output_Parameters) / [来源 2](https://google.github.io/styleguide/cppguide.html#Reference_Arguments) / [来源 3](https://google.github.io/styleguide/cppguide.html#Rvalue_references)
> - [F.15: Prefer simple and conventional ways of passing information](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rf-conventional)
>   - 分类 1：拷贝代价低、不可拷贝（一般传 值）
>   - 分类 2：移动代价低、移动代价中、通用类型
>   - 分类 3：移动代价高（一般传 指针/引用）
> - 不为空的输入参数：
>   - `T` 可变 / `const T&` 不变（[F.16: For “in” parameters, pass cheaply-copied types by value and others by reference to `const`](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rf-in)）
>   - 一般不需要 `const T` 参数（Google Style 没有限制，参考：[sec|Use of `const`/`constexpr`]）
> - 可为空的输入参数：
>   - `T*` 可变 / `const T*` 不变（[F.60: Prefer `T*` over `T&` when “no argument” is a valid option](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rf-ptr-ref)）
> - 右值引用参数：
>   - `T&&`
>   - 被移动的参数（[F.18: For “will-move-from” parameters, pass by `X&&` and `std::move` the parameter](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rf-consume)）
>   - 需转发的参数（[F.19: For “forward” parameters, pass by `TP&&` and only `std::forward` the parameter](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rf-forward)）
> - 输入/输出参数：
>   - `T*`（Google Style）
>   - `T&`（[F.17: For “in-out” parameters, pass by reference to non-`const`](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rf-inout)）
> - 输出参数：
>   - `T*`（Google Style）
>   - 不提倡，可通过 返回值 输出结果（[F.20: For “out” output values, prefer return values to output parameters](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rf-out)）
>   - 不提倡，可通过 多个返回值 输出结果（[F.21: To return multiple “out” values, prefer returning a struct or tuple](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rf-out-multi)）
>   - 可能需要判空，容易遗漏输出逻辑

---

### Smart Pointers Ownership

``` cpp
class Foo {
 private:
  std::unique_ptr<T> owned_;   // Good
  std::shared_ptr<T> shared_;  // Good
  std::weak_ptr<T> referred_;  // Good
  T* referred_without_check_;  // Good
  std::shared_ptr<T> owned_;   // Bad
  T* owned_or_shared_;         // Bad
};
```

> - [来源](https://google.github.io/styleguide/cppguide.html#Ownership_and_Smart_Pointers)
> - [R.20: Use `unique_ptr` or `shared_ptr` to represent ownership](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-owner)
> - [R.21: Prefer `unique_ptr` over `shared_ptr` unless you need to share ownership](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-unique)
> - [R.24: Use `std::weak_ptr` to break cycles of `shared_ptr`s](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-weak_ptr)
> - 避免直接使用 `new`/`delete`：
>   - [R.22: Use `make_shared()` to make `shared_ptr`s](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-make_shared)
>   - [R.23: Use `make_unique()` to make `unique_ptr`s](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-make_unique)

---

### Smart Pointers Parameters

``` cpp
void Foo(
  /* const */ T*,              // refer
  std::unique_ptr<T>,          // own
  std::unique_ptr<T>&,         // reseat
  const std::unique_ptr<T>&,   // Bad
  std::shared_ptr<T>,          // share
  std::shared_ptr<T>&,         // reseat?
  const std::shared_ptr<T>&);  // share?
```

> - [来源](https://google.github.io/styleguide/cppguide.html#Ownership_and_Smart_Pointers)
> - [R.30: Take smart pointers as parameters only to explicitly express lifetime semantics](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-smartptrparam)
> - [R.32: Take a `unique_ptr<widget>` parameter to express that a function assumes ownership of a `widget`](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-uniqueptrparam)
> - [R.33: Take a `unique_ptr<widget>&` parameter to express that a function reseats the `widget`](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-reseat)（Google Style 不允许，改用指针）
> - [R.34: Take a `shared_ptr<widget>` parameter to express that a function is part owner](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-sharedptrparam-owner)
> - [R.35: Take a `shared_ptr<widget>&` parameter to express that a function might reseat the shared pointer](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-sharedptrparam)（Google Style 不允许，改用指针）
> - [R.36: Take a `const shared_ptr<widget>&` parameter to express that it might retain a reference count to the object ???](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-sharedptrparam-const)
> - 返回值 原则相同

---

### Lambda expressions

``` cpp
void Foo::Bar() {
  Baz baz;     // local variable
  std::async(  // async invocation
    [&] { Use(baz); }          // Bad
    [=] { Use(baz); }          // Bad
    [this, baz] { Use(baz); }  // Good?
    [q = Qux()] { q.QFn(); }   // Bad?
  );  // - `Use(baz)` is `Foo::Use(baz)`
}     // - `Qux()` is not `Foo::Qux()`
```

> - [来源](https://google.github.io/styleguide/cppguide.html#Lambda_expressions)
> - [F.50: Use a lambda when a function won’t do (to capture local variables, or to write a local function)](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rf-capture-vs-overload)
>   - 不要滥用全局 lambda（如果可以定义函数）
>   - 一个问题在于 `__FUNCTION__` 只能拿到 `operator() const`
> - [F.52: Prefer capturing by reference in lambdas that will be used locally, including passed to algorithms](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rf-reference-capture)
> - [F.53: Avoid capturing by reference in lambdas that will be used nonlocally, including returned, stored on the heap, or passed to another thread](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rf-value-capture)（参考：[回调时上下文会不会失效](../2019/Inside-Cpp-Callback.md#回调时（弱引用）上下文会不会失效)）
> - [F.54: If you capture `this`, capture all variables explicitly (no default capture)](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rf-this-capture)
> - 不要滥用 初始化捕获 _(init capture)_
>   - 如果不依赖于 闭包作用域 _(enclosing scope)_，可以推迟到 lambda 内构造（但要考虑一份还是多份）
>   - 仅用于 `std::move()` 不可拷贝的对象（参考：[sec|MoveOnly Types]）

---

### Exceptions

``` cpp
try {
  LOG(INFO) << x;   // may throw?
  MayThrowFoo();    // may throw Foo!
  Deserialize(y);   // exception no stack
  auto* p = Get();  // null or throw?
  auto c = a / b;   // crash if |b| is 0
} catch (const Bar& bar) {
  // uncaught, and throw to caller...
}
```

> - [来源](https://google.github.io/styleguide/cppguide.html#Exceptions)
> - 反方观点：避免使用异常，使用显式的错误处理，降低心智负担
>   - 是否会抛出异常 不能在 编译时检查 ??
>   - 抛出异常的类型 不能在 编译时检查 ??
>   - 难以确定 抛出来源（默认只有 `.what()`，没有 `.stack()`）
>     - 例如 隐式转换 [`std::string detail = json_object;`](https://github.com/nlohmann/json#implicit-conversions)（忘了加 `.dump()`）抛出异常 `[json.exception.type_error.302] type must be string, but is object`
>     - 因为 一般认为此处不会抛异常，但又被外层 `try-catch` 捕获，导致无法定位来源（[未捕获的异常 一般可以看到调用栈](https://gcc.gnu.org/bugzilla/show_bug.cgi?id=55917)）
>     - 另外 上层逻辑往往不希望看到 最原始的异常，而希望拿到 更有意义的异常（例如 `type of |json_object| must be string, but is object`）
>   - 容易混淆 异常 和 错误
>     - 例如 `const Value& Path::resolve(const Value& root) const;` 可能 [抛异常](https://github.com/open-source-parsers/jsoncpp/blob/7165f6ac4c482e68475c9e1dac086f9e12fff0d0/src/lib_json/json_value.cpp#L1417)，也可能 [返回 null 的 singleton 引用](https://github.com/open-source-parsers/jsoncpp/blob/ddabf50f72cf369bf652a95c4d9fe31a1865a781/src/lib_json/json_value.cpp#L1597)
>   - 容易混淆 异常 和 契约（参考：[sec|Contracts]）
>     - [ES.105: Don’t divide by zero](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Res-zero)
> - 正方观点：[NR.3: Don’t avoid exceptions](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rnr-no-exceptions)

---

### Run-Time Type Information (RTTI)

``` cpp
if (Derived* derived =
        dynamic_cast<Derived*>(base)) {
  Foo(derived);  // #1
} else {
  Foo(base);     // #2
}

void Base::Foo() { /* #2 */ }
void Derived::Foo() { /* #1 */ }
```

> - [来源](https://google.github.io/styleguide/cppguide.html#Run-Time_Type_Information__RTTI_)
> - 反方观点：[C.153: Prefer virtual function to casting](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rh-use-virtual)
>   - 不符合 面向对象设计，应该避免使用 `typeid` 检查类型 或 `dynamic_cast` 向下转换（以及 type-tag 和 `static_cast`），可以改为：
>     - 用 虚函数多态 实现 单分派 _(single dispatch)_
>     - 用 [访问者模式](../2017/Design-Patterns-Notes-3.md#Visitor) 实现 双分派 _(double dispatch)_
>   - 类型假设随时可能失效（错误使用 `static_cast` 造成内存不对齐，[可能导致崩溃](../2019/Crash-Analysis-Notes.md)）
> - 正方观点：[C.146: Use `dynamic_cast` where class hierarchy navigation is unavoidable](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rh-dynamic_cast)
>   - [C.147: Use `dynamic_cast` to a reference type when failure to find the required class is considered an error](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rh-ref-cast)（Google Style 不允许，禁用异常）
>   - [C.148: Use `dynamic_cast` to a pointer type when failure to find the required class is considered a valid alternative](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rh-ptr-cast)（参考：[Capability Query](https://en.wikibooks.org/wiki/More_C%2B%2B_Idioms/Capability_Query)）
>   - 用于实现 [Acyclic Visitor](https://condor.depaul.edu/dmumaugh/OOT/Design-Principles/acv.pdf)（Robert C. Martin 提出）

---

### Line Length: 80 columns

``` cpp
if (...) {
    while (...) {
        if (...) {
            if (...) break; else return;
        }
        switch(...) {
            break; ... continue; }
    }
}
```

> - [来源](https://google.github.io/styleguide/cppguide.html#Line_Length)
> - [![如何重构“箭头型”代码](asset/63ebf65e54c511ebbab4b05cdaef25a2.jpg)](https://coolshell.cn/articles/17757.html)
> - 如果超过 80 列，先检查：
>   - 格式上，是否存在 4 空格缩进？`namespace` 缩进（参考：[sec|Namespaces]）？
>   - 逻辑上，是否存在 箭头型代码？callback hell？
> - 尤其是 `while/for` 嵌套的 `switch`：
>   - `break` 作用于 `switch`
>   - `continue` 作用于 `while/for`

---

### Naming & Formatting


[img=max-width:88%]

[![一张图总结 Google C++ 编程规范](asset/67b8358254c511ebb25db05cdaef25a2.png)](https://blog.csdn.net/voidccc/article/details/37599203)

> - [来源 1](https://google.github.io/styleguide/cppguide.html#Naming) / [来源 2](https://google.github.io/styleguide/cppguide.html#Formatting)
> - 命名需要熟悉，格式需要自动化

---



## Chromium Style

---

### Variable Initialization

``` cpp
int i = 1;
std::string s = "Hello";
std::pair<bool, double> p = {true, 2.0};
std::vector<int> v = {1, 2, 3};

Foo foo(1.7, false, "test");
std::vector<double> v(500, 0.97);

Bar bar{std::string()};  // explicit ctor
```

> - [来源](https://github.com/chromium/chromium/blob/master/styleguide/c++/c++-dos-and-donts.md#variable-initialization)
> - 优先级：赋值写法 > 构造写法 > C++ 11 `{}` 写法（仅当前两种写法不可用时，例如 `Bar bar(std::string());` 会导致 [most vexing parse](https://www.fluentcpp.com/2018/01/30/most-vexing-parse/) 歧义）
> - 不同观点：
>   - Google Style [没有限制](https://google.github.io/styleguide/cppguide.html#Variable_and_Array_Initialization)
>   - [ES.23: Prefer the `{}`-initializer syntax](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Res-list)

---

### In-class Initializers

``` cpp
class Foo {
 public:
  Foo() : b_(42) { /* empty */ }  // Bad
  Foo(int b) : b_(b) {}  // set |b_|
 private:
  int b_ = 42;           // use |b| or 42
  std::string c_;        // default ctor
  Bar<Foo> bar_{this};   // use |this|
};
```

> - [来源](https://github.com/chromium/chromium/blob/master/styleguide/c++/c++-dos-and-donts.md#initialize-members-in-the-declaration-where-possible)
> - [C.45: Don’t define a default constructor that only initializes data members; use member initializers instead](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rc-default)
> - [C.48: Prefer in-class initializers to member initializers in constructors for constant initializers](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rc-in-class-initializer)

---

### Prefer `=default`

``` cpp
class Foo {
 public:
  Foo();  // non-inlined defined below
  Foo(const Foo&) = default;     // Good
  Foo(/* const */ Foo&);         // Bad
  virtual void operator=(Foo&);  // Bad
  Foo(Foo&&) /* noexcept */;     // Bad
};
Foo::Foo() = default;  // Good for pImpl
```

> - [来源](https://github.com/chromium/chromium/blob/master/styleguide/c++/c++-dos-and-donts.md#prefer-to-use-default)
> - [C.80: Use `=default` if you have to be explicit about using the default semantics](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rc-eqdefault)
> - 拷贝构造函数 参数 `const T&` 容易误写为 `T&`
>   - 导致 [无法重载右值参数](../2018/Cpp-Rvalue-Reference.md#引用参数重载优先级)（编译器允许？）
> - 赋值函数 更容易写错：
>   - 定义为 `virtual`/参数为 `T&`/不返回 `T&`
>     - [C.60: Make copy assignment non-`virtual`, take the parameter by `const&`, and return by non-`const&`](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rc-copy-assignment)
>     - [C.63: Make move assignment non-`virtual`, take the parameter by `&&`, and return by non-`const&`](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rc-move-assignment)
>   - 没检查参数是否 ` == this`
>     - [C.62: Make copy assignment safe for self-assignment](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rc-copy-self)
>     - [C.65: Make move assignment safe for self-assignment](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rc-move-self)
> - 移动构造函数 容易漏掉 `noexcept`（`=default` 会自动加上）
>   - [C.66: Make move operations `noexcept`](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rc-move-noexcept)
>   - 导致 [不能高效使用标准库和语言工具](../2018/Cpp-Rvalue-Reference.md#误解：手写错误的移动构造函数)
> - [I.27: For stable library ABI, consider the Pimpl idiom](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Ri-pimpl)

---

### `auto* p = ...;`

``` cpp
auto  item = item_.get();  // Bad
auto* item = item_.get();  // Good
```

> - [来源](https://github.com/chromium/chromium/blob/master/styleguide/c++/c++-dos-and-donts.md#do-not-use-auto-to-deduce-a-raw-pointer)
> - 增强可读性 + 检查 `item` 必须为 指针类型
> - [Beware unnecessary copies with `auto`](https://llvm.org/docs/CodingStandards.html#beware-unnecessary-copies-with-auto)


### Comment Style

``` cpp
// TODO(botman): use FooImpl as FooBase.
// FooFunction() modifies |foo_member_|.
```

> - [来源](https://github.com/chromium/chromium/blob/master/styleguide/c++/c++-dos-and-donts.md#comment-style)
> - `TODO(xxx)` 待办 要关联信息（[Google Style](https://google.github.io/styleguide/cppguide.html#TODO_Comments)）
> - `FooImpl`/`FooBase` 类名
> - `FooFunction` 函数后加 `()`
> - `foo_member_` 变量外加 `||`

---



## Core Guidelines

---

### Intent

``` cpp
int index = -1;                   // Bad
for (int i = 0; i < v.size(); ++i) {
  if (v[i] == val) {  // compare     Bad
    index = i;        // set index   Bad
    break;            // terminate   Bad
  }
}
auto iter = std::find(            // Good
    std::begin(v), std::end(v), val);
```

> - [P.1: Express ideas directly in code](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rp-direct)
> - [P.3: Express intent](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rp-what)
> - [NL.1: Don’t say in comments what can be clearly stated in code](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rl-comments)
> - 封装统一的 [`base::Contains(c, v)`](https://github.com/chromium/chromium/blob/master/base/stl_util.h) 语义：
>   - 字符串 `s.find(v) != S::npos`
>   - 线性容器 `std::find(c, v) != c.end()`
>   - 关联容器 `c.find(v) != c.end()`（[P0458R2](http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p0458r2.html)）
> - [Turn Predicate Loops into Predicate Functions](http://llvm.org/docs/CodingStandards.html#turn-predicate-loops-into-predicate-functions)

---

### Names and Scopes

``` cpp
auto i = GetStartIndex();
for (i = ; i != ; ++i) {}       // Bad

for (auto i = ; i != ; ++i) {}  // Good

if (auto foo = GetFoo()) {      // Good
  Reuse(i);                     // Bad
  Bar i = foo->GetBar();        // Bad
} else { /* handle nullptr */ }
```

> - [ES.5: Keep scopes small](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Res-scope)
> - [ES.6: Declare names in for-statement initializers and conditions to limit scope](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Res-cond)
> - [ES.12: Do not reuse names in nested scopes](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Res-reuse)
> - [ES.26: Don’t use a variable for two unrelated purposes](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Res-recycle)
> - 参考：[sec|Local Variables]

---

### Virtual Destructors

``` cpp
class Strategy {
 public:
  virtual ~Strategy() = default;
};

class Observer {
 protected:
  ~Observer() = default;
};
```

> - [C.35: A base class destructor should be either public and virtual, or protected and nonvirtual](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rc-dtor-virtual)
> - [C.127: A class with a virtual function should have a virtual or protected destructor](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rh-dtor)
> - 设计虚基类时，一定要考虑：
>   - `public virtual` 析构
>     - 使用者 管理 [`Strategy`](../2017/Design-Patterns-Notes-3.md#Strategy) 生命周期
>     - 例如 `std::unique_ptr<Strategy>` 存储策略对象（参考：[sec|Smart Pointers Ownership]）
>   - `protected non-virtual` 析构
>     - 使用者 仅使用 [`Observer`](../2017/Design-Patterns-Notes-3.md#Observer) 接口
>     - 例如 `std::vector<Observer*>` 记录观察者列表

---

### Polymorphic Classes Slicing

``` cpp
auto  base = derived;            // Bad
auto* base = derived->clone();   // Good
void PolyFoo(      Base  base);  // Bad
void PolyFoo(      Base* base);  // Good
void PolyFoo(const Base& base);  // Good
std::vector<Base>  foos;         // Bad
std::vector<Base*> foos;         // Good
std::vector<std::unique_ptr<Base>> foos;
                                 // Good
```

> - [ES.63: Don’t slice](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Res-slice)
> - [C.67: A polymorphic class should suppress copying](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rc-copy-virtual)
> - [C.130: For making deep copies of polymorphic classes prefer a virtual clone function instead of copy construction/assignment](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rh-copy)
> - [C.145: Access polymorphic objects through pointers and references](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rh-poly)
> - 设计多态类时，一定要考虑：
>   - [sec|Copyable Types (Movable)]
>   - [sec|Copyable Types (Not Movable)]
>   - [sec|MoveOnly Types]
>   - [sec|Not Copyable Or Movable Types]（常用 [`DISALLOW_COPY_AND_ASSIGN`](https://github.com/chromium/chromium/blob/master/base/macros.h)）

---

### RAII

``` cpp
// Bad
FILE* file = fopen(filename, mode);
if (...) return;
if (...) throw XXX;
fclose(file);  // maybe unreachable, leak

// Good (or use std::fstream)
std::unique_ptr<FILE, decltype(fclose)*>
    file(fopen(filename, mode), fclose);
```

> - [R.1: Manage resources automatically using resource handles and RAII (Resource Acquisition Is Initialization)](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-raii)
> - [E.19: Use a final_action object to express cleanup if no suitable resource handle is available](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Re-finally)

---

### Smart Pointers Dangling

``` cpp
std::shared_ptr<Bar> Foo::bar() const;

void f(const Foo& foo) {    // aliased
  UseBarPtr(foo.bar().get());   // Bad
  foo.bar()->IBar();            // Bad
  auto pinned = foo.bar();  // pinned
  UseBarPtr(pinned.get());      // Good
  pinned->IBar();               // Good
}
```

> - [来源](https://google.github.io/styleguide/cppguide.html#Ownership_and_Smart_Pointers)
> - [R.37: Do not pass a pointer or reference obtained from an aliased smart pointer](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Rr-smartptrget)
>   - 仅在 多线程/协程 等并发环境下可能悬垂
>   - `std::shared_ptr` 通过 原子性引用计数 _(atomic ref-count)_ 保证 引用对象的析构过程 线程安全

---

### Contracts

``` cpp
double sqrt(unsigned x) {  // Bad
  Expects(x >= 0);         // Good
  // ...
}
void Foo() {
  // ...
  memset(buffer, 0, kMax);
  Ensures(buffer[0] == 0);
}
```

> - [I.5: State preconditions (if any)](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Ri-pre)
> - [I.6: Prefer `Expects()` for expressing preconditions](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Ri-expects)
> - [I.7: State postconditions](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Ri-post)
> - [I.8: Prefer `Ensures()` for expressing postconditions](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Ri-ensures)
> - [ES.106: Don’t try to avoid negative values by using `unsigned`](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Res-nonnegative)（参考：[数值溢出检查](../2019/Cpp-Check.md#数值溢出检查)，注意 underflow）

---

### Lambda for Complex Initialization

``` cpp
using Map = std::map<
    int, std::unique_ptr<Foo>>;
// cannot use Map{ {1, bar}, {2, baz}, }
const Map foo_map = [] {
  Map r;
  r.emplace(1, std::make_unique<Bar>());
  r.emplace(2, std::make_unique<Baz>());
  return r;
}();
```

> - [ES.28: Use lambdas for complex initialization, especially of `const` variables](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Res-lambda-init)
> - 不能直接用 C++ 11 `{}` 写法构造（因为 `std::unique_ptr` 不可拷贝）

---

