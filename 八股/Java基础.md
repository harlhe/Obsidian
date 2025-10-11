---
title: "Java基础面试题"
source: "https://xiaolincoding.com/interview/java.html"
author:
  - "[[小林coding]]"
published: undefined
created: 2025-09-04
description:
tags:
  - "clippings"
---

## 概念

### 说一下Java的特点

主要有以下的特点：
- **平台无关性** ：Java编译器将源代码编译成字节码（bytecode），该字节码可以在任何安装了Java虚拟机（JVM）的系统上运行。
- **面向对象** 
- **内存管理** ：Java有自己的垃圾回收机制，自动管理内存和回收不再使用的对象

### Java为什么是跨平台的？

Java 能支持跨平台，主要依赖于 JVM ，编写的Java源码，编译后会生成字节码文件。JVM负责将字节码文件翻译成特定平台下的机器码然后运行。

Java代码首先被编译成字节码文件，再由JVM将字节码文件翻译成机器语言，从而达到运行Java程序的目的。
不同平台下编译生成的字节码是一样的，但是由JVM翻译成的机器码却不一样。
JVM是用C/C++开发的，是编译后的机器码，不能跨平台，不同平台下需要安装不同版本的JVM。

![img](https://cdn.xiaolincoding.com//picgo/1713860588639-bb89fc8e-30b6-4d18-a329-f3fea52c729a.png)

### JVM、JDK、JRE三者关系？

![image-20240725230247664](https://cdn.xiaolincoding.com//picgo/image-20240725230247664.png)

它们之间的关系如下：

- JVM是Java虚拟机，是Java程序运行的环境。它负责将Java字节码（由Java编译器生成）解释或编译成机器码，并执行程序。JVM提供了内存管理、垃圾回收、安全性等功能，使得Java程序具备跨平台性。
- JDK是Java开发工具包，是开发Java程序所需的工具集合。它包含了JVM、编译器（javac）、调试器（jdb）等开发工具，以及一系列的类库（如Java标准库和开发工具库）。JDK提供了开发、编译、调试和运行Java程序所需的全部工具和环境。
- JRE是Java运行时环境，是Java程序运行所需的最小环境。它包含了JVM和一组Java类库，用于支持Java程序的执行。JRE不包含开发工具，只提供Java程序运行所需的运行环境。

### 为什么Java解释和编译都有？

首先在Java经过编译之后生成字节码文件，接下来进入JVM中，就有两个步骤编译和解释。 如下图：

![img](https://cdn.xiaolincoding.com//picgo/1715928000183-44fc6130-8abc-4f0b-8f6d-79de0ab09509.webp)

**编译性** ：
- Java源代码首先被编译成字节码，JIT 会把编译过的机器码保存起来,以备下次使用。
**解释性：**
- JVM中一个方法调用计数器，当累计计数大于一定值的时候，就使用JIT进行编译生成机器码文件。否则就是用解释器进行解释执行，然后字节码也是经过解释器进行解释运行的。
所以Java既是编译型也是解释性语言，默认采用的是解释器和编译器混合的模式。
### jvm是什么

JVM是 java 虚拟机，主要工作是解释自己的指令集（即字节码）并映射到本地的CPU指令集和OS的系统调用。
### 为什么用bigDecimal 不用double ？

double会出现精度丢失的问题，double执行的是二进制浮点运算，二进制有些情况下不能准确的表示一个小数。而 Decimal 是精确计算

这样的使用 `BigDecimal` 可以确保精确的十进制数值计算，避免了使用 `double` 可能出现的舍入误差。需要注意的是，在创建 `BigDecimal` 对象时，应该使用字符串作为参数，而不是直接使用浮点数值，以避免浮点数精度丢失。

### 装箱和拆箱是什么？

装箱（Boxing）和拆箱（Unboxing）是将基本数据类型和对应的包装类之间进行转换的过程。

```
Integer i = 10;  //装箱
int n = i;   //拆箱
```

自动装箱主要发生在两种情况，一种是赋值时，另一种是在方法调用的时候。

> 赋值时

这是最常见的一种情况，在Java 1.5以前我们需要手动地进行转换才行，而现在所有的转换都是由编译器来完成。

```
//before autoboxing
Integer iObject = Integer.valueOf(3);
Int iPrimitive = iObject.intValue()

//after java5
Integer iObject = 3; //autobxing - primitive to wrapper conversion
int iPrimitive = iObject; //unboxing - object to primitive conversion
```

> 方法调用时

当我们在方法调用时，我们可以传入原始数据值或者对象，同样编译器会帮我们进行转换。

```java
public static Integer show(Integer iParam){
   System.out.println("autoboxing example - method invocation i: " + iParam);
   return iParam;
}

//autoboxing and unboxing in method invocation
show(3); //autoboxing
int result = show(3); //unboxing because return type of method is Integer
```

show方法接受Integer对象作为参数，当调用 `show(3)` 时，会将int值转换成对应的Integer对象，这就是所谓的自动装箱，show方法返回Integer对象，而 `int result = show(3);`中result为int类型，所以这时候发生自动拆箱操作，将show方法的返回的Integer对象转换成int值。

> 自动装箱的弊端

自动装箱有一个问题，那就是在一个循环中进行自动装箱操作的情况，如下面的例子就会创建多余的对象，影响程序的性能。

```java
Integer sum = 0; for(int i=1000; i<5000; i++){   sum+=i; }
```

上面的代码 `sum+=i` 可以看成 `sum = sum + i` ，但是 `+` 这个操作符不适用于Integer对象，首先sum进行自动拆箱操作，进行数值相加操作，最后发生自动装箱操作转换成Integer对象。其内部变化如下

```java
int result = sum.intValue() + i; Integer sum = new Integer(result);
```

由于我们这里声明的sum为Integer类型，在上面的循环中会创建将近4000个无用的Integer对象，在这样庞大的循环中，会降低程序的性能并且加重了垃圾回收的工作量。因此在我们编程时，需要注意到这一点，正确地声明变量类型，避免因为自动装箱引起的性能问题。

### Java为什么要有Integer？

Integer对应是int类型的包装类，就是把int类型包装成Object对象，可以把数据跟处理这些数据的方法结合在一起，比如Integer就有parseInt()等方法来专门处理int型相关的数据。

在Java中，泛型只能使用引用类型，而不能使用基本类型

在Java中，基本类型和引用类型不能直接进行转换，必须使用包装类来实现。

Java集合中只能存储对象，而不能存储基本数据类型。
### Integer相比int有什么优点？

int是Java中的原始数据类型，而Integer是int的包装类。

Integer和 int 的区别：

- 基本类型和引用类型：首先，int是一种基本数据类型，而Integer是一种引用类型。基本数据类型是Java中最基本的数据类型，它们是预定义的，不需要实例化就可以使用。而引用类型则需要通过实例化对象来使用。这意味着，使用int来存储一个整数时，不需要任何额外的内存分配，而使用Integer时，必须为对象分配内存。在性能方面，基本数据类型的操作通常比相应的引用类型快。
- 自动装箱和拆箱：其次，Integer作为int的包装类，它可以实现自动装箱和拆箱。自动装箱是指将基本类型转化为相应的包装类类型，而自动拆箱则是将包装类类型转化为相应的基本类型。这使得Java程序员更加方便地进行数据类型转换。例如，当我们需要将int类型的值赋给Integer变量时，Java可以自动地将int类型转换为Integer类型。同样地，当我们需要将Integer类型的值赋给int变量时，Java可以自动地将Integer类型转换为int类型。
- 空指针异常：另外，int变量可以直接赋值为0，而Integer变量必须通过实例化对象来赋值。如果对一个未经初始化的Integer变量进行操作，就会出现空指针异常。这是因为它被赋予了null值，而null值是无法进行自动拆箱的。

### 那为什么还要保留int类型？

包装类是引用类型，对象的引用和对象本身是分开存储的，而对于基本类型数据，变量对应的内存块直接存储数据本身。

因此，基本类型数据在读写效率方面，要比包装类高效。除此之外，在64位JVM上，在开启引用压缩的情况下，一个Integer对象占用16个字节的内存空间，而一个int类型数据只占用4字节的内存空间，前者对空间的占用是后者的4倍。

也就是说，不管是读写效率，还是存储效率，基本类型都比包装类高效。
### integer为什么是16字节
一个Java对象在内存中的布局通常由三部分组成：**对象头（Object Header）**、**实例数据（Instance Data）** 和 **对齐填充（Padding）**。
- **Mark Word（标记字段）**: **8字节**
    
    - 这部分用于存储对象自身的运行时数据，如哈希码（HashCode）、GC分代年龄、锁状态标志（偏向锁、轻量级锁、重量级锁）、线程持有的锁等。在64位JVM上，它固定占用8个字节。
        
- **Klass Pointer（类型指针）**: **4字节**
    
    - 这个指针指向方法区中该对象所属的类元数据（Integer.class）。
        
    - 在64位系统上，一个指针原本需要8个字节。但由于开启了**指针压缩**（Compressed Oops），JVM可以用4个字节来表示一个原本需要8个字节的指针，从而节省了大量内存。因此，Klass Pointer在这里只占用4个字节。
对象头总大小 = 8字节（Mark Word） + 4字节（Klass Pointer） = **12字节**
- **int value**: **4字节**
    
    - int是Java的基本数据类型，无论是在32位还是64位JVM上，它都固定占用4个字节。
HotSpot JVM要求对象的起始地址必须是8字节的整数倍。这样做是为了提高内存的访问效率。

- **当前总大小**: 12字节（对象头） + 4字节（实例数据） = **16字节**。
    
- **检查对齐**: 16是8的整数倍（16 % 8 == 0）。
    
- **结论**: 当前大小已经满足8字节对齐的要求，因此不需要额外的字节进行填充。对齐填充为**0字节**。
### 说一下 integer的缓存

Java的Integer类内部实现了一个静态缓存池，用于存储特定范围内的整数值对应的Integer对象。

默认情况下，这个范围是-128至127。当通过Integer.valueOf(int)方法创建一个在这个范围内的整数对象时，并不会每次都生成新的对象实例，而是复用缓存中的现有对象，会直接从内存中取出，不需要新建一个对象。

## 面向对象

### 怎么理解面向对象？简单说说封装继承多态

面向对象是一种编程范式，它 **将现实世界中的事物抽象为对象** ，对象具有属性（称为字段或属性）和行为（称为方法）。

Java面向对象的三大特性包括： **封装、继承、多态** ：

- **封装** ：封装是指将对象的属性（数据）和行为（方法）结合在一起，对外隐藏对象的内部细节，仅通过对象提供的接口与外界交互。封装的目的是增强安全性和简化编程，使得对象更加独立。
- **继承** ：继承是一种可以使得子类自动共享父类数据结构和方法的机制。它是代码复用的重要手段，通过继承可以建立类与类之间的层次关系，使得结构更加清晰。
- **多态** ：多态是指允许不同类的对象对同一消息作出响应。即同一个接口，使用不同的实例而执行不同操作。多态性可以分为编译时多态（重载）和运行时多态（重写）。它使得程序具有良好的灵活性和扩展性。

### 多态体现在哪几个方面？

多态在面向对象编程中可以体现在以下几个方面：

- **方法重载：**
	- 方法重载是指同一类中可以有多个同名方法，它们具有不同的参数列表（参数类型、数量或顺序不同）。虽然方法名相同，但根据传入的参数不同，编译器会在编译时确定调用哪个方法。
	- 示例：对于一个 `add` 方法，可以定义为 `add(int a, int b)` 和 `add(double a, double b)` 。
- **方法重写：**
	- 方法重写是指子类能够提供对父类中同名方法的具体实现。在运行时，JVM会根据对象的实际类型确定调用哪个版本的方法。这是实现多态的主要方式。
	- 示例：在一个动物类中，定义一个 `sound` 方法，子类 `Dog` 可以重写该方法以实现 `bark` ，而 `Cat` 可以实现 `meow` 。
- **接口与实现：**
	- 多态也体现在接口的使用上，多个类可以实现同一个接口，并且用接口类型的引用来调用这些类的方法。这使得程序在面对不同具体实现时保持一贯的调用方式。
	- 示例：多个类（如 `Dog`, `Cat` ）都实现了一个 `Animal` 接口，当用 `Animal` 类型的引用来调用 `makeSound` 方法时，会触发对应的实现。
- **向上转型和向下转型：**
	- 在Java中，可以使用父类类型的引用指向子类对象，这是向上转型。通过这种方式，可以在运行时期采用不同的子类实现。
	- 向下转型是将父类引用转回其子类类型，但在执行前需要确认引用实际指向的对象类型以避免 `ClassCastException` 。

### 多态解决了什么问题？

多态是指子类可以替换父类，在实际的代码运行过程中，调用子类的方法实现。多态这种特性也需要编程语言提供特殊的语法机制来实现，比如继承、接口类。

多态可以提高代码的扩展性和复用性，是很多设计模式、设计原则、编程技巧的代码实现基础。比如策略模式、基于接口而非实现编程、依赖倒置原则、里式替换原则、利用多态去掉冗长的 if-else 语句等等

### 面向对象的设计原则你知道有哪些吗

面向对象编程中的六大原则：

- **单一职责原则（SRP）** ：一个类应该只有一个引起它变化的原因，即一个类应该只负责一项职责。例子：考虑一个员工类，它应该只负责管理员工信息，而不应负责其他无关工作。
- **开放封闭原则（OCP）** ：软件实体应该对扩展开放，对修改封闭。例子：通过制定接口来实现这一原则，比如定义一个图形类，然后让不同类型的图形继承这个类，而不需要修改图形类本身。
- **里氏替换原则（LSP）** ：子类对象应该能够替换掉所有父类对象。例子：一个正方形是一个矩形，但如果修改一个矩形的高度和宽度时，正方形的行为应该如何改变就是一个违反里氏替换原则的例子。
- **接口隔离原则（ISP）** ：客户端不应该依赖那些它不需要的接口，即接口应该小而专。例子：通过接口抽象层来实现底层和高层模块之间的解耦，比如使用依赖注入。
- **依赖倒置原则（DIP）** ：高层模块不应该依赖低层模块，二者都应该依赖于抽象；抽象不应该依赖于细节，细节应该依赖于抽象。例子：如果一个公司类包含部门类，应该考虑使用合成/聚合关系，而不是将公司类继承自部门类。
- **最少知识原则 (Law of Demeter)** ：一个对象应当对其他对象有最少的了解，只与其直接的朋友交互。

### 重载与重写有什么区别？

- 重载（Overloading）指的是在同一个类中，可以有多个同名方法，它们具有不同的参数列表（参数类型、参数个数或参数顺序不同），编译器根据调用时的参数类型来决定调用哪个方法。
- 重写（Overriding）指的是子类可以重新定义父类中的方法，方法名、参数列表和返回类型必须与父类中的方法一致，通过@override注解来明确表示这是对父类方法的重写。

重载是指在同一个类中定义多个同名方法，而重写是指子类重新定义父类中的方法。

### 抽象类和普通类区别？

| 特性/方面                   | 抽象类 (Abstract Class)                                                     | 普通类 (Normal Class)                       |
| ----------------------- | ------------------------------------------------------------------------ | ---------------------------------------- |
| **实例化 (Instantiation)** | **不能**被实例化。你不能使用 `new` 关键字直接创建一个抽象类的对象。                                  | **可以**被实例化。你可以自由地使用 `new` 关键字创建它的对象。     |
| **方法 (Methods)**        | 既可以包含**具体方法**（有方法体），也可以包含**抽象方法**（没有方法体，用 `abstract` 关键字修饰）。             | **只能**包含**具体方法**，所有方法都必须有完整的方法体。         |
| **构造方法 (Constructor)**  | **有**构造方法。但它不是用来创建自身实例的，而是在子类创建实例时，由子类的构造方法调用，用于初始化从父类继承的成员。             | **有**构造方法，主要作用就是在创建该类的实例时进行初始化。          |
| **继承 (Inheritance)**    | 专门为了被继承而设计。子类使用 `extends` 继承它，并且**必须实现**父类中所有的抽象方法（除非子类自己也是一个抽象类）。       | 也可以被继承，子类可以选择性地重写（Override）父类的方法，没有强制要求。 |
| **关键字 (Keyword)**       | 使用 `abstract` 关键字来声明。                                                    | 不需要任何特殊关键字来声明。                           |
| **设计目的**                | 主要用于**代码复用**和**模板设计**。它为一组相关的子类提供一个共同的基类，定义了它们的通用结构和行为规范，强制子类去实现某些特定的行为。 | 主要作为具体事物的实现，用于创建可以直接使用的对象，完成具体的功能。       |

### Java抽象类和接口的区别是什么？

**两者的特点：**

- 抽象类用于描述类的共同特性和行为，可以有成员变量、构造方法和具体方法。适用于有明显继承关系的场景。
- 接口用于定义行为规范，可以多实现，只能有常量和抽象方法（Java 8 以后可以有默认方法和静态方法）。适用于定义类的能力或功能。

**两者的区别：**

| 特性/方面     | 抽象类 (Abstract Class)                                              | 接口 (Interface)                                                                                                   |
| --------- | ----------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| **继承/实现** | 使用 `extends` 关键字继承，**只能单继承**。                                     | 使用 `implements` 关键字实现，**可以多实现**。                                                                                 |
| **设计理念**  | **is-a (是一个)** 关系，体现的是一种继承关系，强调根源的相似性。                            | **can-do (能做到)** 关系，体现的是一种行为规范或能力，强调功能的实现。                                                                       |
| **成员变量**  | 可以包含各种类型的成员变量（实例变量、静态变量），可以有不同的访问修饰符（public, protected, private）。 | **Java 8 之前**：只能包含 `public static final` 类型的常量。<br>**Java 8 之后**：规则不变，仍是公共静态常量。                                  |
| **方法**    | 可以包含**抽象方法**和**具体方法**（有方法体的方法）。                                   | **Java 8 之前**：只能包含 `public abstract` 方法。<br>**Java 8 之后**：可以额外包含 `default` (默认) 方法和 `static` (静态) private（私有）方法。 |
| **构造方法**  | **有**构造方法，但不能用于创建自身实例，主要用于子类构造器调用以完成初始化。                          | **没有**构造方法。                                                                                                      |
| **访问修饰符** | 方法和变量可以是 `public`, `protected`, `private`。                        | 方法默认是 `public`，变量默认是 `public static final`。                                                                      |

### 抽象类能加final修饰吗？

**不能** ，Java中的抽象类是用来被继承的，而final修饰符用于禁止类被继承或方法被重写，因此，抽象类和final修饰符是互斥的，不能同时使用。
因为abstract就是为了必须继承，所以涉及的都不能用final修饰。
抽象方法不能用final，非抽象方法可以用final修饰。

### 接口里面可以定义哪些方法？

- **抽象方法**

抽象方法是接口的核心部分，所有实现接口的类都必须实现这些方法。抽象方法默认是 public 和 abstract，这些修饰符可以省略。

```java
public interface Animal {
    void makeSound();
}
```
- **默认方法**

默认方法是在 Java 8 中引入的，允许接口提供具体实现。实现类可以选择重写默认方法。

```java
public interface Animal {
    void makeSound();
    
    default void sleep() {
        System.out.println("Sleeping...");
    }
}
```
- **静态方法**

静态方法也是在 Java 8 中引入的，它们属于接口本身，可以通过接口名直接调用，而不需要实现类的对象。

```java
public interface Animal {
    void makeSound();
    
    static void staticMethod() {
        System.out.println("Static method in interface");
    }
}
```
- **私有方法**

私有方法是在 Java 9 中引入的，用于在接口中为默认方法或其他私有方法提供辅助功能。这些方法不能被实现类访问，只能在接口内部使用。

```java
public interface Animal {
    void makeSound();
    
    default void sleep() {
        System.out.println("Sleeping...");
        logSleep();
    }
    
    private void logSleep() {
        System.out.println("Logging sleep");
    }
}
```
```java
public interface Animal {
    void makeSound();
}
```

### 抽象类可以被实例化吗？

在Java中，抽象类本身不能被实例化。

这意味着不能使用 `new` 关键字直接创建一个抽象类的对象。抽象类的存在主要是为了被继承，它通常包含一个或多个抽象方法（由 `abstract` 关键字修饰且无方法体的方法），这些方法需要在子类中被实现。

抽象类可以有构造器，这些构造器在子类实例化时会被调用，以便进行必要的初始化工作。然而，这个过程并不是直接实例化抽象类，而是创建了子类的实例，间接地使用了抽象类的构造器。

例如：

```java
public abstract class AbstractClass {
    public AbstractClass() {
        // 构造器代码
    }
    
    public abstract void abstractMethod();
}

public class ConcreteClass extends AbstractClass {
    public ConcreteClass() {
        super(); // 调用抽象类的构造器
    }
    
    @Override
    public void abstractMethod() {
        // 实现抽象方法
    }
}

// 下面的代码可以运行
ConcreteClass obj = new ConcreteClass();
```

在这个例子中， `ConcreteClass` 继承了 `AbstractClass` 并实现了抽象方法 `abstractMethod()` 。当我们创建 `ConcreteClass` 的实例时， `AbstractClass` 的构造器被调用，但这并不意味着 `AbstractClass` 被实例化；实际上，我们创建的是 `ConcreteClass` 的一个对象。

简而言之，抽象类不能直接实例化，但通过继承抽象类并实现所有抽象方法的子类是可以被实例化的。

### 接口可以包含构造函数吗？

在接口中，不可以有构造方法,在接口里写入构造方法时，编译器提示：Interfaces cannot have constructors，因为接口不会有自己的实例的，所以不需要有构造函数。

为什么呢？构造函数就是初始化class的属性或者方法，在new的一瞬间自动调用，那么问题来了Java的接口，都不能new 那么要构造函数干嘛呢？根本就没法调用

### 解释Java中的静态变量和静态方法

在Java中，静态变量和静态方法是与类本身关联的，而不是与类的实例（对象）关联。它们在内存中只存在一份，可以被类的所有实例共享。

> 静态变量

静态变量（也称为类变量）是在类中使用 `static` 关键字声明的变量。它们属于类而不是任何具体的对象。主要的特点：

- **共享性** ：所有该类的实例共享同一个静态变量。如果一个实例修改了静态变量的值，其他实例也会看到这个更改。
- **初始化** ：静态变量在类被加载时初始化，只会对其进行一次分配内存。
- **访问方式** ：静态变量可以直接通过类名访问，也可以通过实例访问，但推荐使用类名。

示例：

```java
public class MyClass {
    static int staticVar = 0; // 静态变量

    public MyClass() {
        staticVar++; // 每创建一个对象，静态变量自增
    }
    
    public static void printStaticVar() {
        System.out.println("Static Var: " + staticVar);
    }
}

// 使用示例
MyClass obj1 = new MyClass();
MyClass obj2 = new MyClass();
MyClass.printStaticVar(); // 输出 Static Var: 2
```

> 静态方法

静态方法是在类中使用 `static` 关键字声明的方法。类似于静态变量，静态方法也属于类，而不是任何具体的对象。主要的特点：

- **无实例依赖** ：静态方法可以在没有创建类实例的情况下调用。对于静态方法来说，不能直接访问非静态的成员变量或方法，因为静态方法没有上下文的实例。
- **访问静态成员** ：静态方法可以直接调用其他静态变量和静态方法，但不能直接访问非静态成员。
- **多态性** ：静态方法不支持重写（Override），但可以被隐藏（Hide）。
```java
public class MyClass {
    static int count = 0;

    // 静态方法
    public static void incrementCount() {
        count++;
    }

    public static void displayCount() {
        System.out.println("Count: " + count);
    }
}

// 使用示例
MyClass.incrementCount(); // 调用静态方法
MyClass.displayCount();   // 输出 Count: 1
```

> 使用场景

- **静态变量** ：常用于需要在所有对象间共享的数据，如计数器、常量等。
- **静态方法** ：常用于助手方法（utility methods）、获取类级别的信息或者是没有依赖于实例的数据处理。

### 非静态内部类和静态内部类的区别？

区别包括：

- 非静态内部类依赖于外部类的实例，而静态内部类不依赖于外部类的实例。
- 非静态内部类可以访问外部类的实例变量和方法，而静态内部类只能访问外部类的静态成员。
- 非静态内部类不能定义静态成员，而静态内部类可以定义静态成员。
- 非静态内部类在外部类实例化后才能实例化，而静态内部类可以独立实例化。
- 非静态内部类可以访问外部类的私有成员，而静态内部类不能直接访问外部类的私有成员，需要通过实例化外部类来访问。

### 非静态内部类可以直接访问外部方法，编译器是怎么做到的？

非静态内部类可以直接访问外部方法是因为编译器在生成字节码时会为非静态内部类维护一个指向外部类实例的引用。

这个引用使得非静态内部类能够访问外部类的实例变量和方法。编译器会在生成非静态内部类的构造方法时，将外部类实例作为参数传入，并在内部类的实例化过程中建立外部类实例与内部类实例之间的联系，从而实现直接访问外部方法的功能。

## 关键字

### Java 中 final 作用是什么？

`final` 关键字主要有以下三个方面的作用：用于修饰类、方法和变量。

- 修饰类：当 `final` 修饰一个类时，表示这个类不能被继承，Java 中的 `String` 类就是用 `final` 修饰的，这保证了 `String` 类的不可变性和安全性，防止其他类通过继承来改变 `String` 类的行为和特性。
- 修饰方法：用 `final` 修饰的方法不能在子类中被重写。比如， `java.lang.Object` 类中的 `getClass` 方法就是 `final` 的，因为这个方法的行为是由 Java 虚拟机底层实现来保证的，不应该被子类修改。
- 修饰变量：当 `final` 修饰基本数据类型的变量时，该变量一旦被赋值就不能再改变。例如， `final int num = 10;`，这里的 `num` 就是一个常量，不能再对其进行重新赋值操作，否则会导致编译错误。对于引用数据类型， `final` 修饰意味着这个引用变量不能再指向其他对象，但对象本身的内容是可以改变的。例如， `final StringBuilder sb = new StringBuilder("Hello");`，不能让 `sb` 再指向其他 `StringBuilder` 对象，但可以通过 `sb.append(" World");`来修改字符串的内容。

### Java 中 static的作用是什么？

`static` 关键字主要用于修饰类的成员（变量、方法、代码块）和内部类，其核心作用是 **将成员与类本身关联，而非与类的实例（对象）关联** 。具体作用如下：

> 1、修饰变量

被 `static` 修饰的变量属于类本身，而非类的某个实例。所有对象共享同一份静态变量，内存中只存在一份副本。可以通过 `类名.变量名` 直接访问，无需创建对象（也可通过对象访问，但不推荐）。

通常用于存储所有对象共享的数据，如常量、计数器等。

```java
public class Student {
    // 静态变量（所有学生共享同一个学校名称）
    public static String schoolName = "阳光中学";
    // 实例变量（每个学生有自己的姓名）
    private String name;
}

// 访问静态变量
public class Test {
    public static void main(String[] args) {
        System.out.println(Student.schoolName); // 直接通过类名访问
    }
}
```

> 2、修饰方法

静态方法属于类，不属于任何实例，因此 **不能直接访问类中的非静态成员（变量 / 方法）** （因为非静态成员依赖于对象存在），但可以访问静态成员。通过 `类名.方法名` 直接调用，无需创建对象。

通常用于工具类方法（如 `Math.random()` ）、工厂方法等，不需要依赖对象状态即可完成操作。

```java
public class MathUtils {
    // 静态方法（无需创建对象即可调用）
    public static int add(int a, int b) {
        return a + b;
    }
}

// 调用静态方法
public class Test {
    public static void main(String[] args) {
        int result = MathUtils.add(2, 3); // 直接通过类名调用
    }
}
```

> 3、修饰代码块

静态代码块在 **类加载时执行** ，且只执行一次（优于对象构造方法），用于初始化静态变量或执行类级别的预处理操作。

多个静态代码块按定义顺序执行，且先于非静态代码块和构造方法。

```java
public class Database {
    private static String url;
    
    // 静态代码块：初始化静态变量
    static {
        url = "jdbc:mysql://localhost:3306/test";
        System.out.println("数据库连接地址初始化完成");
    }
}
```

> 4、修饰内部类

静态内部类不依赖于外部类的实例，可以独立存在， **不能直接访问外部类的非静态成员** （需通过外部类实例访问）。

当内部类与外部类的实例无关时使用，避免内部类持有外部类的引用导致的内存泄漏。

```java
public class OuterClass {
    private static int staticVar = 10;
    private int instanceVar = 20;
    
    // 静态内部类
    public static class StaticInnerClass {
        public void print() {
            System.out.println(staticVar); // 可访问外部类静态变量
            // System.out.println(instanceVar); // 错误：不能直接访问非静态变量
        }
    }
}

// 使用静态内部类
public class Test {
    public static void main(String[] args) {
        OuterClass.StaticInnerClass inner = new OuterClass.StaticInnerClass();
        inner.print();
    }
}
```

## 深拷贝和浅拷贝

### 深拷贝和浅拷贝的区别？

![img](https://cdn.xiaolincoding.com//picgo/1720683675376-c5af6668-4538-479f-84e8-42d4143ab101.webp)

- 浅拷贝是指只复制对象本身和其内部的值类型字段，但不会复制对象内部的引用类型字段。换句话说，浅拷贝只是创建一个新的对象，然后将原对象的字段值复制到新对象中，但如果原对象内部有引用类型的字段，只是将引用复制到新对象中，两个对象指向的是同一个引用对象。
- 深拷贝是指在复制对象的同时，将对象内部的所有引用类型字段的内容也复制一份，而不是共享引用。换句话说，深拷贝会递归复制对象内部所有引用类型的字段，生成一个全新的对象以及其内部的所有对象。

### 实现深拷贝的三种方法是什么？

在 Java 中，实现对象深拷贝的方法有以下几种主要方式：

> 实现 Cloneable 接口并重写 clone() 方法

这种方法要求对象及其所有引用类型字段都实现 Cloneable 接口，并且重写 clone() 方法。在 clone() 方法中，通过递归克隆引用类型字段来实现深拷贝。

```java
class MyClass implements Cloneable {
    private String field1;
    private NestedClass nestedObject;

    @Override
    protected Object clone() throws CloneNotSupportedException {
        MyClass cloned = (MyClass) super.clone();
        cloned.nestedObject = (NestedClass) nestedObject.clone(); // 深拷贝内部的引用对象
        return cloned;
    }
}

class NestedClass implements Cloneable {
    private int nestedField;

    @Override
    protected Object clone() throws CloneNotSupportedException {
        return super.clone();
    }
}
```

> 使用序列化和反序列化

通过将对象序列化为字节流，再从字节流反序列化为对象来实现深拷贝。要求对象及其所有引用类型字段都实现 Serializable 接口。

```java
import java.io.*;

class MyClass implements Serializable {
    private String field1;
    private NestedClass nestedObject;

    public MyClass deepCopy() {
        try {
            ByteArrayOutputStream bos = new ByteArrayOutputStream();
            ObjectOutputStream oos = new ObjectOutputStream(bos);
            oos.writeObject(this);
            oos.flush();
            oos.close();

            ByteArrayInputStream bis = new ByteArrayInputStream(bos.toByteArray());
            ObjectInputStream ois = new ObjectInputStream(bis);
            return (MyClass) ois.readObject();
        } catch (IOException | ClassNotFoundException e) {
            e.printStackTrace();
            return null;
        }
    }
}

class NestedClass implements Serializable {
    private int nestedField;
}
```

> 手动递归复制

针对特定对象结构，手动递归复制对象及其引用类型字段。适用于对象结构复杂度不高的情况。

```java
class MyClass {
    private String field1;
    private NestedClass nestedObject;

    public MyClass deepCopy() {
        MyClass copy = new MyClass();
        copy.setField1(this.field1);
        copy.setNestedObject(this.nestedObject.deepCopy());
        return copy;
    }
}

class NestedClass {
    private int nestedField;

    public NestedClass deepCopy() {
        NestedClass copy = new NestedClass();
        copy.setNestedField(this.nestedField);
        return copy;
    }
}
```

## 泛型

### 什么是泛型？

泛型是 Java 编程语言中的一个重要特性，它允许类、接口和方法在定义时使用一个或多个类型参数，这些类型参数在使用时可以被指定为具体的类型。

泛型的主要目的是在编译时提供更强的类型检查，并且在编译后能够保留类型信息，避免了在运行时出现类型转换异常。

> 为什么需要泛型？

- **适用于多种数据类型执行相同的代码**
```java
private static int add(int a, int b) {
    System.out.println(a + "+" + b + "=" + (a + b));
    return a + b;
}

private static float add(float a, float b) {
    System.out.println(a + "+" + b + "=" + (a + b));
    return a + b;
}

private static double add(double a, double b) {
    System.out.println(a + "+" + b + "=" + (a + b));
    return a + b;
}
```

如果没有泛型，要实现不同类型的加法，每种类型都需要重载一个add方法；通过泛型，我们可以复用为一个方法：

```java
private static <T extends Number> double add(T a, T b) {
    System.out.println(a + "+" + b + "=" + (a.doubleValue() + b.doubleValue()));
    return a.doubleValue() + b.doubleValue();
}
```
- **泛型中的类型在使用时指定，不需要强制类型转换** （ **类型安全** ，编译器会 **检查类型** ）

看下这个例子：

```java
List list = new ArrayList();
list.add("xxString");
list.add(100d);
list.add(new Person());
```

我们在使用上述list中，list中的元素都是Object类型（无法约束其中的类型），所以在取出集合元素时需要人为的强制类型转化到具体的目标类型，且很容易出现java.lang.ClassCastException异常。

引入泛型，它将提供类型的约束，提供编译前的检查：

```java
List<String> list = new ArrayList<String>();

// list中只能放String, 不能放其它类型的元素
```

## 对象

### java创建对象有哪些方式？

在Java中，创建对象的方式有多种，常见的包括：

**1、使用new关键字** ：这是最常见、最基础的创建对象方式。通过调用类的构造器来实例化对象。

```java
// 定义一个类
public class Person {
    private String name;
    
    public Person() {} // 默认构造器
    public Person(String name) { // 带参构造器
        this.name = name;
    }
    
    public void sayHello() {
        System.out.println("Hello, " + name);
    }
}

// 使用 new 创建对象
public class Main {
    public static void main(String[] args) {
        Person person1 = new Person(); // 调用无参构造
        Person person2 = new Person("Alice"); // 调用有参构造
        
        person2.sayHello(); // 输出: Hello, Alice
    }
}
```

优点是简单、直接、明确。缺点是紧密耦合，必须知道具体的类名。

**2、使用Class类的newInstance()方法** ：通过 Java 的反射 API，在运行时动态地创建对象。这种方式不需要在编译时知道具体的类。

```java
注意：Class.newInstance() 在 JDK 9 后被标记为过时，因为它只能调用无参公有构造器，且会抛出所有异常。Constructor.newInstance() 更强大、更灵活。MyClass obj = (MyClass) Class.forName("com.example.MyClass").newInstance();
```

应用场景：框架设计（如 Spring 的 IOC 容器）、动态代理等。

**注意** ： `Class.newInstance()` 在 JDK 9 后被标记为过时，因为它只能调用无参公有构造器，且会抛出所有异常。 `Constructor.newInstance()` 更强大、更灵活。

**使用Constructor类的newInstance()方法** ：同样是通过反射机制，可以使用Constructor类的newInstance()方法创建对象。

```java
Constructor<MyClass> constructor = MyClass.class.getConstructor();
MyClass obj = constructor.newInstance();
```

**3、使用clone()方法** ：通过实现 `Cloneable` 接口并重写 `Object` 类的 `clone()` 方法，可以基于一个现有对象（原型）创建一个新的副本对象。

```java
// 实现 Cloneable 接口
public class Person implements Cloneable {
    private String name;
    
    // ... 构造器和其他方法 ...
    
    @Override
    protected Object clone() throws CloneNotSupportedException {
        return super.clone(); // 浅拷贝
    }
}

public class Main {
    public static void main(String[] args) {
        Person original = new Person("Charlie");
        try {
            Person copy = (Person) original.clone(); // 创建副本
            copy.sayHello(); // 输出: Hello, Charlie
        } catch (CloneNotSupportedException e) {
            e.printStackTrace();
        }
    }
}
```

`Object.clone()` 默认是浅拷贝，对于引用类型的字段，复制的是引用地址，而不是引用的对象本身。如果需要深拷贝，必须在 `clone()` 方法中手动对引用对象进行克隆。

**4、使用反序列化** ：通过 `ObjectInputStream` 从一个字节流（通常是文件或网络）中重建一个对象。

```java
import java.io.*;

// 必须实现 Serializable 接口
public class Person implements Serializable {
    private String name;
    // ... 构造器和其他方法 ...
}

public class Main {
    public static void main(String[] args) {
        Person personToSave = new Person("David");
        
        // 序列化对象到文件
        try (ObjectOutputStream oos = new ObjectOutputStream(new FileOutputStream("person.dat"))) {
            oos.writeObject(personToSave);
        } catch (IOException e) {
            e.printStackTrace();
        }
        
        // 从文件反序列化对象
        try (ObjectInputStream ois = new ObjectInputStream(new FileInputStream("person.dat"))) {
            Person restoredPerson = (Person) ois.readObject(); // 创建新对象
            restoredPerson.sayHello(); // 输出: Hello, David
        } catch (IOException | ClassNotFoundException e) {
            e.printStackTrace();
        }
    }
}
```

特点是不会调用类的任何构造器，类必须实现 `java.io.Serializable` 接口。

**5、使用工厂模式** ：这是一种设计模式，不直接使用 `new` ，而是通过一个方法来返回对象实例。 `getInstance()` 、 `valueOf()` 等都是常见的工厂方法。

```java
public class Person {
    private String name;
    
    private Person(String name) { // 构造器可以是私有的
        this.name = name;
    }
    
    // 静态工厂方法
    public static Person createPerson(String name) {
        // 这里可以做一些额外的逻辑，比如缓存、日志、返回子类实例等
        return new Person(name);
    }
}

public class Main {
    public static void main(String[] args) {
        // 不是用 new，而是用工厂方法创建
        Person person = Person.createPerson("Eva");
        person.sayHello();
    }
}
```

优点是将对象的创建与使用分离，降低耦合，还可以隐藏创建对象的复杂逻辑（如池化技术、缓存）。

Java 标准库中的例子： `Integer.valueOf(int)` ， `Calendar.getInstance()` 。

最后来个，总结对比：

| 方式 | 核心原理 | 是否调用构造器？ | 特点与应用场景 |
| --- | --- | --- | --- |
| **`new` 关键字** | JVM 指令 | **是** | 最标准、最常用，紧密耦合 |
| **反射** | 运行时类信息 | **是** (`Constructor`) | 灵活，解耦，用于框架 |
| **`clone()`** | 复制现有对象 | **否** | 基于原型创建副本，需实现 `Cloneable` |
| **反序列化** | 从字节流恢复 | **否** | 用于持久化和网络通信，需实现 `Serializable` |
| **工厂模式** | 方法封装 `new` | **是** (在方法内) | 解耦，隐藏创建逻辑，控制实例 |

### Java创建对象除了new还有别的什么方式?

- **通过反射创建对象** ：通过 Java 的反射机制可以在运行时动态地创建对象。可以使用 Class 类的 newInstance() 方法或者通过 Constructor 类来创建对象。
```java
public class MyClass {
    public MyClass() {
        // Constructor
    }
}

public class Main {
    public static void main(String[] args) throws Exception {
        Class<?> clazz = MyClass.class;
        MyClass obj = (MyClass) clazz.newInstance();
    }
}
```
- **通过反序列化创建对象** ：通过将对象序列化（保存到文件或网络传输）然后再反序列化（从文件或网络传输中读取对象）的方式来创建对象，对象能被序列化和反序列化的前提是类实现Serializable接口。
```java
import java.io.*;

public class MyClass implements Serializable {
    // Class definition
}

public class Main {
    public static void main(String[] args) throws Exception {
        // Serialize object
        MyClass obj = new MyClass();
        ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream("object.ser"));
        out.writeObject(obj);
        out.close();
        
        // Deserialize object
        ObjectInputStream in = new ObjectInputStream(new FileInputStream("object.ser"));
        MyClass newObj = (MyClass) in.readObject();
        in.close();
    }
}
```
- **通过clone创建对象** ：所有 Java 对象都继承自 Object 类，Object 类中有一个 clone() 方法，可以用来创建对象的副本，要使用 clone 方法，我们必须先实现 Cloneable 接口并实现其定义的 clone 方法。
```java
public class MyClass implements Cloneable {
    @Override
    public Object clone() throws CloneNotSupportedException {
        return super.clone();
    }
}

public class Main {
    public static void main(String[] args) throws CloneNotSupportedException {
        MyClass obj1 = new MyClass();
        MyClass obj2 = (MyClass) obj1.clone();
    }
}
```

### New出的对象什么时候回收？

通过过关键字 `new` 创建的对象，由Java的垃圾回收器（Garbage Collector）负责回收。垃圾回收器的工作是在程序运行过程中自动进行的，它会周期性地检测不再被引用的对象，并将其回收释放内存。

具体来说，Java对象的回收时机是由垃圾回收器根据一些算法来决定的，主要有以下几种情况：

1. 引用计数法：某个对象的引用计数为0时，表示该对象不再被引用，可以被回收。
2. 可达性分析算法：从根对象（如方法区中的类静态属性、方法中的局部变量等）出发，通过对象之间的引用链进行遍历，如果存在一条引用链到达某个对象，则说明该对象是可达的，反之不可达，不可达的对象将被回收。
3. 终结器（Finalizer）：如果对象重写了 `finalize()` 方法，垃圾回收器会在回收该对象之前调用 `finalize()` 方法，对象可以在 `finalize()` 方法中进行一些清理操作。然而，终结器机制的使用不被推荐，因为它的执行时间是不确定的，可能会导致不可预测的性能问题。

### 如何获取私有对象？

在 Java 中，私有对象通常指的是类中被声明为 `private` 的成员变量或方法。由于 `private` 访问修饰符的限制，这些成员只能在其所在的类内部被访问。

不过，可以通过下面两种方式来间接获取私有对象。

- 使用公共访问器方法（getter 方法）：如果类的设计者遵循良好的编程规范，通常会为私有成员变量提供公共的访问器方法（即 `getter` 方法），通过调用这些方法可以安全地获取私有对象。
```java
class MyClass {
    // 私有成员变量
    private String privateField = "私有字段的值";

    // 公共的 getter 方法
    public String getPrivateField() {
        return privateField;
    }
}

public class Main {
    public static void main(String[] args) {
        MyClass obj = new MyClass();
        // 通过调用 getter 方法获取私有对象
        String value = obj.getPrivateField();
        System.out.println(value); 
    }
}
```
- 反射机制。反射机制允许在运行时检查和修改类、方法、字段等信息，通过反射可以绕过 `private` 访问修饰符的限制来获取私有对象。
```java
import java.lang.reflect.Field;

class MyClass {
    private String privateField = "私有字段的值";
}

public class Main {
    public static void main(String[] args) throws NoSuchFieldException, IllegalAccessException {
        MyClass obj = new MyClass();
        // 获取 Class 对象
        Class<?> clazz = obj.getClass();
        // 获取私有字段
        Field privateField = clazz.getDeclaredField("privateField");
        // 设置可访问性
        privateField.setAccessible(true);
        // 获取私有字段的值
        String value = (String) privateField.get(obj);
        System.out.println(value); 
    }
}
```

## 反射

### 什么是反射？

Java 反射机制是在运行状态中，对于任意一个类，都能够知道这个类中的所有属性和方法，对于任意一个对象，都能够调用它的任意一个方法和属性；这种动态获取的信息以及动态调用对象的方法的功能称为 Java 语言的反射机制。

反射具有以下特性：

1. **运行时类信息访问** ：反射机制允许程序在运行时获取类的完整结构信息，包括类名、包名、父类、实现的接口、构造函数、方法和字段等。
2. **动态对象创建** ：可以使用反射API动态地创建对象实例，即使在编译时不知道具体的类名。这是通过Class类的newInstance()方法或Constructor对象的newInstance()方法实现的。
3. **动态方法调用** ：可以在运行时动态地调用对象的方法，包括私有方法。这通过Method类的invoke()方法实现，允许你传入对象实例和参数值来执行方法。
4. **访问和修改字段值** ：反射还允许程序在运行时访问和修改对象的字段值，即使是私有的。这是通过Field类的get()和set()方法完成的。

![img](https://cdn.xiaolincoding.com//picgo/1718957173277-863d2ec6-a754-423b-9066-9f28610d1a31.png)

### 反射在你平时写代码或者框架中的应用场景有哪些?

> 加载数据库驱动

我们的项目底层数据库有时是用mysql，有时用oracle，需要动态地根据实际情况加载驱动类，这个时候反射就有用了，假设 com.mikechen.java.myqlConnection，com.mikechen.java.oracleConnection这两个类我们要用。

这时候我们在使用 JDBC 连接数据库时使用 Class.forName()通过反射加载数据库的驱动程序，如果是mysql则传入mysql的驱动类，而如果是oracle则传入的参数就变成另一个了。

> 配置文件加载

Spring 框架的 IOC（动态加载管理 Bean），Spring通过配置文件配置各种各样的bean，你需要用到哪些bean就配哪些，spring容器就会根据你的需求去动态加载，你的程序就能健壮地运行。

Spring通过XML配置模式装载Bean的过程：

- 将程序中所有XML或properties配置文件加载入内存
- Java类里面解析xml或者properties里面的内容，得到对应实体类的字节码字符串以及相关的属性信息
- 使用反射机制，根据这个字符串获得某个类的Class实例
- 动态配置实例的属性

配置文件

```java
className=com.example.reflectdemo.TestInvoke
methodName=printlnState
```

实体类

```java
public class TestInvoke {
    private void printlnState(){
        System.out.println("I am fine");
    }
}
```

解析配置文件内容

```java
// 解析xml或properties里面的内容，得到对应实体类的字节码字符串以及属性信息
public static String getName(String key) throws IOException {
    Properties properties = new Properties();
    FileInputStream in = new FileInputStream("D:\IdeaProjects\AllDemos\language-specification\src\main\resources\application.properties");
    properties.load(in);
    in.close();
    return properties.getProperty(key);
}
```

利用反射获取实体类的Class实例，创建实体类的实例对象，调用方法

```java
public static void main(String[] args) throws NoSuchMethodException, InvocationTargetException, IllegalAccessException, IOException, ClassNotFoundException, InstantiationException {
    // 使用反射机制，根据这个字符串获得Class对象
    Class<?> c = Class.forName(getName("className"));
    System.out.println(c.getSimpleName());
    // 获取方法
    Method method = c.getDeclaredMethod(getName("methodName"));
    // 绕过安全检查
    method.setAccessible(true);
    // 创建实例对象
    TestInvoke testInvoke = (TestInvoke)c.newInstance();
    // 调用方法
    method.invoke(testInvoke);

}
```

运行结果：

![img](https://cdn.xiaolincoding.com//picgo/1718786675327-3a60bcc7-2f70-4096-998e-d6e94f5df6a4.png)

## 注解

### 能讲一讲Java注解的原理吗？
你可以把**注解看作是贴在代码（类、方法、字段等）上的“标签”**
**定义一种元数据（标签），然后通过某种机制（工具）在特定的时候（编译期或运行时）去读取这些元数据，并根据元数据执行相应的处理逻辑。**
注解本质是一个继承了Annotation的特殊接口，其具体实现类是Java运行时生成的动态代理类。

我们通过反射获取注解时，返回的是Java运行时生成的动态代理对象。通过代理对象调用自定义注解的方法，会最终调用AnnotationInvocationHandler的invoke方法。该方法会从memberValues这个Map中索引出对应的值。而memberValues的来源是Java常量池。

### 对注解解析的底层实现了解吗？

注解本质上是一种特殊的接口，它继承自 `java.lang.annotation.Annotation` 接口， **所以注解也叫声明式接口** ，例如，定义一个简单的注解：

```java
public @interface MyAnnotation {
    String value();
}
```

编译后，Java 编译器会将其转换为一个继承自 `Annotation` 的接口，并生成相应的字节码文件。
```java

public interface MyAnnotation extends java.lang.annotation.Annotation {
    public abstract String value();
}
```
根据注解的作用范围，Java 注解可以分为以下几种类型：

- **源码级别注解** ：仅存在于源码中，编译后不会保留（ `@Retention(RetentionPolicy.SOURCE)` ）。
- 开发者编写一个继承自 `javax.annotation.processing.AbstractProcessor` 的注解处理器类。，
- 在编译 (`javac`) 过程中编译器会扫描源码，如果发现了被特定注解标记的代码，就会调用对应的注解处理器。
- 注解处理器可以访问到被标记代码的语法树信息，并根据这些信息**生成新的 Java 源码文件**，新生成的源码文件会和你的原始源码一起被编译成 `.class` 文件。
- `@Getter`, `@Setter`, `@Data` 等注解。

- **类文件级别注解** ：保留在 `.class` 文件中，但运行时不可见（ `@Retention(RetentionPolicy.CLASS)` ）。
- 在 `.class` 文件生成后，但在被 JVM 加载前，这些工具可以读取 `.class` 文件中的注解信息，然后动态地修改字节码，织入新的逻辑。
- **AspectJ (AOP 框架)**: 可以在编译后，将切面逻辑（如日志、事务）直接织入到 `.class` 文件的已有方法中，比 Spring AOP（基于运行时代理）的性能更高。
- 

- **运行时注解** ：保留在 `.class` 文件中，并且可以通过反射在运行时访问（ `@Retention(RetentionPolicy.RUNTIME)` ）。
- 通过调用反射对象的 `getAnnotation()`, `isAnnotationPresent()`
- IoC 容器：启动时扫描指定的包，通过反射找到带有 `@Component`, `@Service` 等注解的类，然后实例化它们并放入容器中。
- 依赖注入：扫描到带有 `@Autowired` 的字段或方法，通过反射将容器中的 Bean 实例赋值给它。
- SpringMVC：扫描带有 `@Controller` 的类和带有 `@RequestMapping` 的方法，建立 URL 和方法之间的映射关系。

只有运行时注解可以通过反射机制进行解析。

当注解被标记为 `RUNTIME` 时，Java 编译器会在生成的 `.class` 文件中保存注解信息。这些信息存储在字节码的属性表（Attribute Table）中，具体包括以下内容：

- **RuntimeVisibleAnnotations** ：存储运行时可见的注解信息RUNTIME。
- **RuntimeInvisibleAnnotations** ：存储运行时不可见的注解信息CLASS。
- **RuntimeVisibleParameterAnnotations** 和 **RuntimeInvisibleParameterAnnotations** ：存储方法参数上的注解信息。

通过工具（如 `javap -v` ）可以查看 `.class` 文件中的注解信息。
### 运行时注解是如何解析的？

注解的解析主要依赖于 Java 的反射机制。以下是解析注解的基本流程：

1、获取注册信息：通过反射 API 可以获取类、方法、字段等元素上的注解。例如：

```java
Class<?> clazz = MyClass.class;
MyAnnotation annotation = clazz.getAnnotation(MyAnnotation.class);
if (annotation != null) {
    System.out.println(annotation.value());
}
```

2、底层原理：注解反射机制的核心类是 **`java.lang.reflect.AnnotatedElement`** ，它是所有可以被注解修饰的元素（如 `Class` 、 `Method` 、 `Field` 等）的父接口。该接口提供了以下方法：

- `getAnnotation(Class<T> annotationClass)` ：获取指定类型的注解。
- `getAnnotations()` ：获取所有注解。
- `isAnnotationPresent(Class<? extends Annotation> annotationClass)` ：判断是否包含指定注解。

这些方法的底层实现依赖于 JVM 提供的本地方法（Native Method）

JVM 在加载类时会解析 `.class` 文件中的注解信息，并将其存储在内存中，供反射机制使用。


### Java注解的作用域呢？

1. **类级别作用域**：用于描述类的注解，通常放置在类定义的上面，可以用来指定类的一些属性，如类的访问级别、继承关系、注释等。
2. **方法级别作用域**：用于描述方法的注解，通常放置在方法定义的上面，可以用来指定方法的一些属性，如方法的访问级别、返回值类型、异常类型、注释等。
3. **字段级别作用域**：用于描述字段的注解，通常放置在字段定义的上面，可以用来指定字段的一些属性，如字段的访问级别、默认值、注释等。、
4. **其他级别作用域：** 构造函数作用域和局部变量作用域。用来对构造函数和局部变量进行描述和注释。


## 异常

### 介绍一下Java异常

Java异常类层次结构图： ![img](https://cdn.xiaolincoding.com//picgo/1720683900898-1d0ce69d-4b5d-41a6-a5df-022e42f8f4c5.webp) 
1. **Error（错误）** ：表示运行时环境的错误。错误是程序无法处理的严重问题，如系统崩溃、虚拟机错误、动态链接失败等。通常，程序不应该尝试捕获这类错误。例如，OutOfMemoryError、StackOverflowError等。
2. **Exception（异常）** ：表示程序本身可以处理的异常条件。异常分为两大类：
	- **非运行时异常** ：这类异常在编译时期就必须被捕获或者声明抛出。它们通常是外部错误，如文件不存在（FileNotFoundException）、类未找到（ClassNotFoundException）等。非运行时异常强制程序员处理这些可能出现的问题，增强了程序的健壮性。
	- **运行时异常** ：这类异常包括运行时异常（RuntimeException）和错误（Error）。运行时异常由程序错误导致，如空指针访问（NullPointerException）、数组越界（ArrayIndexOutOfBoundsException）等。运行时异常是不需要在编译时强制捕获或声明的。

### Java异常处理有哪些？

异常处理是通过使用try-catch语句块来捕获和处理异常。以下是Java中常用的异常处理方式：

- try-catch语句块：用于捕获并处理可能抛出的异常。try块中包含可能抛出异常的代码，catch块用于捕获并处理特定类型的异常。可以有多个catch块来处理不同类型的异常。
```java
try {
    // 可能抛出异常的代码
} catch (ExceptionType1 e1) {
    // 处理异常类型1的逻辑
} catch (ExceptionType2 e2) {
    // 处理异常类型2的逻辑
} catch (ExceptionType3 e3) {
    // 处理异常类型3的逻辑
} finally {
    // 可选的finally块，用于定义无论是否发生异常都会执行的代码
}
```
- throw语句：用于手动抛出异常。可以根据需要在代码中使用throw语句主动抛出特定类型的异常。
```
throw new ExceptionType("Exception message");
```
- throws关键字：用于在方法声明中声明可能抛出的异常类型。如果一个方法可能抛出异常，但不想在方法内部进行处理，可以使用throws关键字将异常传递给调用者来处理。
```java
public void methodName() throws ExceptionType {
    // 方法体
}
```
- finally块：用于定义无论是否发生异常都会执行的代码块。通常用于释放资源，确保资源的正确关闭。
```java
try {
    // 可能抛出异常的代码
} catch (ExceptionType e) {
    // 处理异常的逻辑
} finally {
    // 无论是否发生异常，都会执行的代码
}
```

### 抛出异常为什么不用throws？

- **Unchecked Exceptions** ：对于未检查异常（unchecked exceptions）是继承自RuntimeException类或Error类的异常，编译器不强制要求进行异常处理。因此，对于这些异常，不需要在方法签名中使用throws来声明。示例包括NullPointerException、ArrayIndexOutOfBoundsException等。
- **捕获和处理异常** ：更期望在方法内部捕获了可能抛出的异常，并在方法内部处理它们，而不是通过throws子句将它们传递到调用者。这种情况下，方法可以处理异常而无需在方法签名中使用throws。

### try catch中的语句运行情况

try块中的代码将按顺序执行，如果抛出异常，将在catch块中进行匹配和处理，然后程序将继续执行catch块之后的代码。如果没有匹配的catch块，异常将被传递给上一层调用的方法。

### try{return “a”} finally{return “b”}这条语句返回啥

finally块中的return语句会覆盖try块中的return返回，因此，该语句将返回"b"。

## object

### \== 与 equals 有什么区别？

对于字符串变量来说，使用"\=="和"equals"比较字符串时，其比较方法不同。"\=="比较两个变量本身的值，即两个对象在内存中的首地址，"equals"比较字符串包含内容是否相同。

对于非字符串变量来说，如果没有对equals()进行重写的话，"\==" 和 "equals"方法的作用是相同的，都是用来比较对象在堆内存中的首地址，即用来比较两个引用变量是否指向同一个对象。

- \==：比较的是两个字符串内存地址（堆内存）的数值是否相等，属于数值比较；
- equals()：比较的是两个字符串的内容，属于内容比较。

### hashcode和equals方法有什么关系？

在 Java 中，对于重写 `equals` 方法的类，通常也需要重写 `hashCode` 方法，并且需要遵循以下规定：

- **一致性** ：如果两个对象使用 `equals` 方法比较结果为 `true` ，那么它们的 `hashCode` 值必须相同。也就是说，如果 `obj1.equals(obj2)` 返回 `true` ，那么 `obj1.hashCode()` 必须等于 `obj2.hashCode()` 。
- **非一致性** ：如果两个对象的 `hashCode` 值相同，它们使用 `equals` 方法比较的结果不一定为 `true` 。即 `obj1.hashCode() == obj2.hashCode()` 时， `obj1.equals(obj2)` 可能为 `false` ，这种情况称为哈希冲突。

`hashCode` 和 `equals` 方法是紧密相关的，重写 `equals` 方法时必须重写 `hashCode` 方法，以保证在使用哈希表等数据结构时，对象的相等性判断和存储查找操作能够正常工作。而重写 `hashCode` 方法时，需要确保相等的对象具有相同的哈希码，但相同哈希码的对象不一定相等。

### String、StringBuffer、StringBuilder的区别和联系

**1、可变性** ： `String` 是不可变的（Immutable），一旦创建，内容无法修改，每次修改都会生成一个新的对象。 `StringBuilder` 和 `StringBuffer` 是可变的（Mutable），可以直接对字符串内容进行修改而不会创建新对象。

**2、线程安全性** ： `String` 因为不可变，天然线程安全。 `StringBuilder` 不是线程安全的，适用于单线程环境。 `StringBuffer` 是线程安全的，其方法通过 `synchronized` 关键字实现同步，适用于多线程环境。

**3、性能** ： `String` 性能最低，尤其是在频繁修改字符串时会生成大量临时对象，增加内存开销和垃圾回收压力。 `StringBuilder` 性能最高，因为它没有线程安全的开销，适合单线程下的字符串操作。 `StringBuffer` 性能略低于 `StringBuilder` ，因为它的线程安全机制引入了同步开销。

**4、使用场景** ：如果字符串内容固定或不常变化，优先使用 `String` 。如果需要频繁修改字符串且在单线程环境下，使用 `StringBuilder` 。如果需要频繁修改字符串且在多线程环境下，使用 `StringBuffer` 。

对比总结如下：

| **特性** | **String** | **StringBuilder** | **StringBuffer** |
| --- | --- | --- | --- |
| **不可变性** | 不可变 | 可变 | 可变 |
| **线程安全** | 是（因不可变） | 否 | 是（同步方法） |
| **性能** | 低（频繁修改时） | 高（单线程） | 中（多线程安全） |
| **适用场景** | 静态字符串 | 单线程动态字符串 | 多线程动态字符串 |

例子代码如下：

```java
// String的不可变性
String str = "abc";
str = str + "def"; // 新建对象，str指向新对象

// StringBuilder（单线程高效）
StringBuilder sb = new StringBuilder();
sb.append("abc").append("def"); // 直接修改内部数组

// StringBuffer（多线程安全）
StringBuffer sbf = new StringBuffer();
sbf.append("abc").append("def"); // 同步方法保证线程安全
```

## Java 新特性

### Java 8 你知道有什么新特性？

下面是 Java 8 主要新特性的整理表格，包含关键改进和示例说明：

| **特性名称**              | **描述**                                     | **示例或说明**                                                                                |
| --------------------- | ------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **Lambda 表达式**        | 简化匿名内部类，支持函数式编程                            | `(a, b) -> a + b` 代替匿名类实现接口                                                              |
| **函数式接口**             | 仅含一个抽象方法的接口，可用 `@FunctionalInterface` 注解标记 | `Runnable`, `Comparator`, 或自定义接口 `@FunctionalInterface interface MyFunc { void run(); }` |
| **Stream API**        | 提供链式操作处理集合数据，支持并行处理                        | `list.stream().filter(x -> x > 0).collect(Collectors.toList())`                          |
| **Optional 类**        | 封装可能为 `null` 的对象，减少空指针异常                   | `Optional.ofNullable(value).orElse("default")`                                           |
| **方法引用**              | 简化 Lambda 表达式，直接引用现有方法                     | `System.out::println` 等价于 `x -> System.out.println(x)`                                   |
| **接口的默认方法与静态方法**      | 接口可定义默认实现和静态方法，增强扩展性                       | `interface A { default void print() { System.out.println("默认方法"); } }`                   |
| **并行数组排序**            | 使用多线程加速数组排序                                | `Arrays.parallelSort(array)`                                                             |
| **重复注解**              | 允许同一位置多次使用相同注解                             | `@Repeatable` 注解配合容器注解使用                                                                 |
| **类型注解**              | 注解可应用于更多位置（如泛型、异常等）                        | `List<@NonNull String> list`                                                             |
| **CompletableFuture** | 增强异步编程能力，支持链式调用和组合操作                       | `CompletableFuture.supplyAsync(() -> "result").thenAccept(System.out::println)`          |

### Lambda 表达式了解吗？
使用的三个场景：线程runnable匿名内部类，处理集合链式操作stream过滤，函数式编程范式。

Lambda 表达式它是一种简洁的语法，用于创建匿名函数，主要用于简化函数式接口（只有一个抽象方法的接口）的使用。其基本语法有以下两种形式：

- `(parameters) -> expression` ：当 Lambda 体只有一个表达式时使用，表达式的结果会作为返回值。
- `(parameters) -> { statements; }` ：当 Lambda 体包含多条语句时，需要使用大括号将语句括起来，若有返回值则需要使用 `return` 语句。

传统的匿名内部类实现方式代码较为冗长，而 Lambda 表达式可以用更简洁的语法实现相同的功能。比如，使用匿名内部类实现 `Runnable` 接口

```java
public class AnonymousClassExample {
    public static void main(String[] args) {
        Thread t1 = new Thread(new Runnable() {
            @Override
            public void run() {
                System.out.println("Running using anonymous class");
            }
        });
        t1.start();
    }
}
```

使用 Lambda 表达式实现相同功能：

```java
public class LambdaExample {
    public static void main(String[] args) {
        Thread t1 = new Thread(() -> System.out.println("Running using lambda expression"));
        t1.start();
    }
}
```

可以看到，Lambda 表达式的代码更加简洁明了。

还有，Lambda 表达式能够更清晰地表达代码的意图，尤其是在处理集合操作时，如过滤、映射等。比如，过滤出列表中所有偶数

```java
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class ReadabilityExample {
    public static void main(String[] args) {
        List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5, 6);
        // 使用 Lambda 表达式结合 Stream API 过滤偶数
        List<Integer> evenNumbers = numbers.stream()
                                           .filter(n -> n % 2 == 0)
                                           .collect(Collectors.toList());
        System.out.println(evenNumbers);
    }
}
```

通过 Lambda 表达式，代码的逻辑更加直观，易于理解。

还有，Lambda 表达式使得 Java 支持函数式编程范式，允许将函数作为参数传递，从而可以编写更灵活、可复用的代码。比如定义一个通用的计算函数。

```java
interface Calculator {
    int calculate(int a, int b);
}

public class FunctionalProgrammingExample {
    public static int operate(int a, int b, Calculator calculator) {
        return calculator.calculate(a, b);
    }

    public static void main(String[] args) {
        // 使用 Lambda 表达式传递加法函数
        int sum = operate(3, 5, (x, y) -> x + y);
        System.out.println("Sum: " + sum);

        // 使用 Lambda 表达式传递乘法函数
        int product = operate(3, 5, (x, y) -> x * y);
        System.out.println("Product: " + product);
    }
}
```

缺点：增加调试困难，因为 Lambda 表达式是匿名的，在调试时很难定位具体是哪个 Lambda 表达式出现了问题。尤其是当 Lambda 表达式嵌套使用或者比较复杂时，调试难度会进一步增加。

### Java中stream的API介绍一下

Java 8引入了Stream API，它提供了一种高效且易于使用的数据处理方式，特别适合集合对象的操作，如过滤、映射、排序等。Stream API不仅可以提高代码的可读性和简洁性，还能利用多核处理器的优势进行并行处理。让我们通过两个具体的例子来感受下Java Stream API带来的便利，对比在Stream API引入之前的传统做法。
`stream()` 方法主要是在 **`java.util.Collection` 接口**中定义的一个**默认方法**，几乎所有集合都实现了stream接口
> 案例1：过滤并收集满足条件的元素

**问题场景** ：从一个列表中筛选出所有长度大于3的字符串，并收集到一个新的列表中。

**没有Stream API的做法** ：

```java
List<String> originalList = Arrays.asList("apple", "fig", "banana", "kiwi");
List<String> filteredList = new ArrayList<>();

for (String item : originalList) {
    if (item.length() > 3) {
        filteredList.add(item);
    }
}
```

这段代码需要显式地创建一个新的ArrayList，并通过循环遍历原列表，手动检查每个元素是否满足条件，然后添加到新列表中。

**使用Stream API的做法** ：

```java
List<String> originalList = Arrays.asList("apple", "fig", "banana", "kiwi");
List<String> filteredList = originalList.stream()
                                        .filter(s -> s.length() > 3)
                                        .collect(Collectors.toList());
```

这里，我们直接在原始列表上调用`.stream()` 方法创建了一个流，使用`.filter()` 中间操作筛选出长度大于3的字符串，最后使用`.collect(Collectors.toList())` 终端操作将结果收集到一个新的列表中。代码更加简洁明了，逻辑一目了然。

> 案例2：计算列表中所有数字的总和

**问题场景** ：计算一个数字列表中所有元素的总和。

**没有Stream API的做法** ：

```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
int sum = 0;
for (Integer number : numbers) {
    sum += number;
}
```

这个传统的for-each循环遍历列表中的每一个元素，累加它们的值来计算总和。

**使用Stream API的做法** ：

```java
List<Integer> numbers = Arrays.asList(1, 2, 3, 4, 5);
int sum = numbers.stream()
                 .mapToInt(Integer::intValue)
                 .sum();
```

通过Stream API，我们可以先使用`.mapToInt()` 将Integer流转换为IntStream（这是为了高效处理基本类型），然后直接调用`.sum()` 方法来计算总和，极大地简化了代码。

### Stream流的并行API是什么？

是 ParallelStream。

并行流（ParallelStream）就是将源数据分为多个子流对象进行多线程操作，然后将处理的结果再汇总为一个流对象，底层是使用通用的 fork/join 池来实现，即将一个任务拆分成多个“小任务”并行计算，再把多个“小任务”的结果合并成总的计算结果

Stream串行流与并行流的主要区别：

![img](https://cdn.xiaolincoding.com//picgo/1716365522454-4b56a07e-9b54-4cbb-9832-26b099fc35cd.png)

对CPU密集型的任务来说，并行流使用ForkJoinPool线程池，为每个CPU分配一个任务，这是非常有效率的，但是如果任务不是CPU密集的，而是I/O密集的，并且任务数相对线程数比较大，那么直接用ParallelStream并不是很好的选择。

**主要区别对比

| 特性维度       | 串行Stream (Sequential Stream)                                         | 并行Stream (Parallel Stream)                                                                  |
| ---------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| **执行方式**   | **单线程**，在调用Stream操作的那个线程中执行。                                         | **多线程**，默认使用公共的`ForkJoinPool`线程池。                                                           |
| **性能**     | 适用于数据量小、或者每个元素操作非常简单的场景。                                             | 在**多核CPU**上，处理**大数据集**且**每个元素的操作耗时较长（CPU密集型）**时，性能优势明显。                                     |
| **结果顺序**   | **严格保证顺序**。元素的处理顺序和它们在源中的顺序一致。                                       | **不保证顺序**。除非使用`forEachOrdered`等特殊终端操作，否则元素的处理和输出顺序是随机的。                                     |
| **线程安全**   | **通常是线程安全的**，因为所有操作都在一个线程内完成，不存在资源竞争。                                | **需要开发者自己保证线程安全**。如果在并行流中修改共享变量（如往一个共享的`List`中添加元素），必须使用线程安全的集合或同步锁，否则会产生竞态条件，导致结果不正确。      |
| **CPU使用率** | 只会利用一个CPU核心。                                                         | 会充分利用多个CPU核心，CPU使用率会显著上升。                                                                   |
| **适用场景**   | 1. 数据量小<br>2. 元素处理有顺序依赖<br>3. 操作本身是I/O密集型<br>4. 包含需要线程安全的操作但不想处理同步问题 | 1. **CPU密集型**操作（如复杂的数学计算）<br>2. **大数据集**<br>3. 任务可以轻松分解且合并成本低<br>4. Lambda表达式中没有副作用，不修改共享状态 |

### completableFuture怎么用的？

CompletableFuture是由Java 8引入的，在Java8之前我们一般通过Future实现异步。

- Future用于表示异步计算的结果，只能通过阻塞或者轮询的方式获取结果，而且不支持设置回调方法，Java 8之前若要设置回调一般会使用guava的ListenableFuture，回调的引入又会导致臭名昭著的回调地狱（下面的例子会通过ListenableFuture的使用来具体进行展示）。
- CompletableFuture对Future进行了扩展，可以通过设置回调的方式处理计算结果，同时也支持组合操作，支持进一步的编排，同时一定程度解决了回调地狱的问题。
#### 核心设计：Completion 栈（或链表）

##### 1. 存储回调函数
 线程安全
- `CompletableFuture` 对象内部维护着一个数据结构（类似于一个栈或链表），专门用来存放后续需要执行的回调任务。
    
- 当你调用 `.thenApply()`, `.whenComplete()` 等方法时，你传入的函数（Lambda表达式）会被封装成一个任务对象，并被添加到这个内部的回调列表中。
    

##### 2. 完成结果

- 当异步计算任务执行完毕后，会调用 `CompletableFuture` 内部的 `complete()` 或类似方法，将计算结果（或异常）存入 `CompletableFuture` 对象中。
    
- 这个“存入结果”的动作是关键的触发点。
    

##### 3. 触发并执行回调

- 一旦结果被成功存入，`CompletableFuture` 会立即检查其内部的回调列表。
    
- 如果列表不为空，它会遍历这个列表，并使用刚刚存入的结果作为参数，去执行列表中的每一个回调任务。
    
- 执行回调的线程，根据调用的方法（是否带 `Async` 后缀）和任务完成的时机，可能是完成任务的线程，也可能是公共线程池中的线程，或者是当前线程。
    
CompletableFuture的实现如下（`supplyAsync` 用于执行一个带返回值的任务，这个返回的 `CompletableFuture` 对象最终会持有 `Supplier` <`U`>执行后返回的那个 `U` 类型的结果，而 `runAsync` 用于执行一个没有返回值的任务。）：

```java
ExecutorService executor = Executors.newFixedThreadPool(5);
//表示创建一个异步任务
//第一个参数表示一个异步执行lambda的具体逻辑，第二个参数表示cf1异步任务提交的线程池
//CompletableFuture.supplyAsync(Supplier<U> supplier, Executor executor)
CompletableFuture<String> cf1 = CompletableFuture.supplyAsync(() -> {
    System.out.println("执行step 1");
    return "step1 result";
}, executor);
//重载，使用默认的线程池
//CompletableFuture.supplyAsync(Supplier<U> supplier)
CompletableFuture<String> cf2 = CompletableFuture.supplyAsync(() -> {
    System.out.println("执行step 2");
    return "step2 result";
});
//链式调用，thencombine第一个参数是要和cf1结合的另一个completablefuture，第二个参数定义了cf2和cf1都完成之后的动作，result1和2自动接受cf12运行的返回结果，lambda函数的返回作为新的completablefuture对象，同时thenaccept最终阶段，接受thencombine结果
//thenCombine(CompletionStage<? extends U> other, BiFunction<? super T,? super U,? extends V> fn)
//thenAccept(Consumer<? super T> action)接受消费者lambda函数
cf1.thenCombine(cf2, (result1, result2) -> {
    System.out.println(result1 + " , " + result2);
    System.out.println("执行step 3");
    return "step3 result";
}).thenAccept(result3 -> System.out.println(result3));
```

显然，CompletableFuture的实现更为简洁，可读性更好。

![img](https://cdn.xiaolincoding.com//picgo/1713777049912-2268a5fc-c7f1-477d-8c9c-310aae18f51a.png) CompletableFuture实现了两个接口（如上图所示)：Future、CompletionStage。

- Future表示异步计算的结果，CompletionStage用于表示异步执行过程中的一个步骤（Stage），这个步骤可能是由另外一个CompletionStage触发的，随着当前步骤的完成，也可能会触发其他一系列CompletionStage的执行。
- 从而我们可以根据实际业务对这些步骤进行多样化的编排组合，CompletionStage接口正是定义了这样的能力，我们可以通过其提供的thenAppy、thenCompose等函数式编程方法来组合编排这些步骤。

### Java 21 新特性知道哪些？

**新新语言特性：**

- **Switch 语句的模式匹配** ：不需要instenceof匹配对象的类型，作用域在->的右侧。例如，对于不同类型的账户类，可以在 `switch` 语句中直接根据账户类型的模式来获取相应的余额，如 `case savingsAccount sa -> result = sa.getSavings();`
- **数组模式** ：将模式匹配扩展到数组中，例如， `if (arr instanceof int[] {1, 2, 3})`
- **字符串模板（预览版）** ：支持在字符串字面量中直接嵌入表达式。例如，以前可能需要使用 `"hello " + name + ", welcome to the geeksforgeeks!"` 这样的方式来拼接字符串，在 Java 21 中可以使用 `hello {name}, welcome to the geeksforgeeks!`这种更简洁的写法

**新并发特性方面：**

- **虚拟线程** ：这是 Java 21 引入的一种轻量级并发的新选择。它通过共享堆栈的方式，大大降低了内存消耗，同时提高了应用程序的吞吐量和响应速度。可以使用静态构建方法、构建器或 `ExecutorService` 来创建和使用虚拟线程。
- **Scoped Values（范围值）** ：提供了一种在线程间共享不可变数据的新方式，避免使用传统的线程局部存储，促进了更好的封装性和线程安全，可用于在不通过方法参数传递的情况下，传递上下文信息，如用户会话或配置设置。
### 虚拟线程
好的，我们来详细解释一下在 Java 世界中引起巨大反响的**虚拟线程 (Virtual Threads)**。这是 Java 21 (LTS) 中最终定稿的里程碑式功能，源自于著名的 **Loom 项目 (Project Loom)**。

#### 核心思想：一个生动的比喻

要理解虚拟线程，我们先用一个餐厅服务员的比喻：

- **传统线程（平台线程）**： 想象一家餐厅只有 **10 位“精英服务员”**（平台线程）。每个服务员都非常强大，但他们有一个奇怪的规矩：当客人点了一道需要等 20 分钟的菜时（**一个阻塞的 I/O 操作**，如等待数据库返回数据），这位服务员**必须站在桌子旁一动不动地等 20 分钟**，直到菜做好。
    
    - **结果**：很快，10 位服务员都分别被不同的客人“占用”并站在那里干等。餐厅外面排起了长队，但没有服务员能去接待新客人。这家餐厅最多只能同时服务 10 桌客人，效率极低。
        
- **虚拟线程**： 现在，餐厅改变了模式。他们仍然只有 **10 位“精英服务员”**（平台线程），但他们引入了**无数张“电子订单卡”**（虚拟线程）。
    
    - **工作流程**：
        
        1. 一位服务员 A 去为 1 号桌点餐。客人点了一道需要等 20 分钟的菜。
            
        2. 服务员 A 将这个请求（订单卡）提交给厨房（**发起 I/O 请求**），然后**他立刻离开 1 号桌**，把订单卡留在桌上。
            
        3. 服务员 A 立刻去为 2 号桌、3 号桌点餐，继续提交订单给厨房。10 位服务员时刻保持忙碌，不断地在不同餐桌间穿梭、提交订单。
            
        4. 20 分钟后，厨房的显示屏提示 1 号桌的菜好了（**I/O 操作完成**）。
            
        5. **任何一位**当前空闲的服务员（比如服务员 B）看到提示后，拿起 1 号桌的订单卡，将菜送过去。
            
    - **结果**：10 位服务员几乎没有一秒钟是在“干等”，他们的时间被充分利用。这家餐厅现在可以**同时处理成千上万桌客人**的请求，尽管物理上还是只有 10 个服务员在跑腿。
        

---

#### 虚拟线程是什么？

**虚拟线程**是由 JVM 而不是操作系统（OS）管理的**轻量级线程**。它的核心是改变了 Java 线程与操作系统线程之间的关系。

1. **传统线程 (Platform Threads)**
    
    - `java.lang.Thread` 的传统实现。
        
    - 它是一个对**操作系统内核线程**的薄包装。创建一个 Java 平台线程，就意味着在操作系统层面创建了一个昂贵的内核线程。
        
    - **缺点**：
        
        - **资源昂贵**：每个线程都预占了较大的内存（线程栈），创建和销毁开销大。
            
        - **数量有限**：操作系统能创建的线程数量是有限的（通常是几千个）。
            
        - **上下文切换成本高**：线程的调度由操作系统内核负责，切换成本高。
            
2. **虚拟线程 (Virtual Threads)**
    
    - 它不再与操作系统线程一一对应。
        
    - JVM 内部维护了一个**少量平台线程组成的线程池**（这些平台线程被称为**载体线程 Carrier Threads**，也就是比喻中的“服务员”）。
        
    - **成千上万甚至上百万个虚拟线程**可以运行在这个小小的载体线程池之上。JVM 负责将虚拟线程**“挂载 (mount)”** 到载体线程上执行，以及在需要时**“卸载 (unmount)”**。
        

#### 虚拟线程的“魔法”：非阻塞的阻塞

这是虚拟线程最革命性的地方。当一个虚拟线程中的代码执行一个**阻塞 I/O 操作**时（例如，读取网络数据、查询数据库），会发生以下情况：

1. JVM **拦截**了这个阻塞调用。
    
2. JVM **自动将这个虚拟线程从它的载体平台线程上“卸载”下来**，并将其作为一个内部对象保存起来，等待 I/O 操作完成。
    
3. 那个**载体平台线程立刻被释放**，可以去执行另一个准备就绪的虚拟线程。
    

当 I/O 操作完成后（例如，数据库返回了数据），JVM 会将那个被“卸载”的虚拟线程重新提交给调度器，等待被一个空闲的载体平台线程“挂载”并继续执行。

**对开发者的意义**： 你写的代码**看起来是同步阻塞的**，非常简单直观，但其底层的执行方式**却达到了异步非阻塞的性能和吞吐量**。

---

#### 核心优势

1. **极大地提升了吞吐量**
    
    - 对于 I/O 密集型应用（如 Web 服务器、微服务），可以轻松处理数十万甚至上百万的并发连接，而传统模型只能处理几千个。
        
2. **简化了并发编程**
    
    - 开发者不再需要为了性能而编写复杂的异步代码（如 `CompletableFuture` 链式调用、回调地狱）。
        
    - 可以直接使用简单、易于理解和调试的**“一个请求一个线程 (thread-per-request)”**模型。可以用标准的 `try-catch` 处理异常，用普通的循环和条件语句，代码逻辑像单线程一样清晰。
        
3. **资源成本极低**
    
    - 虚拟线程只是一个普通的 Java 对象，占用内存极小（几百字节），创建和切换的成本远低于平台线程。
        

#### 如何使用虚拟线程

Java 21 提供了非常简洁的 API 来创建和使用虚拟线程。

**1. 直接启动一个虚拟线程**

Java

```java
Runnable runnable = () -> System.out.println("在虚拟线程中运行...");
Thread.startVirtualThread(runnable);
```

**2. 使用 ExecutorService (推荐方式)** 这是最常用和推荐的方式，它会为每一个提交的任务创建一个新的虚拟线程。

Java

```java
try (ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor()) {
    for (int i = 0; i < 100_000; i++) {
        int taskIndex = i;
        executor.submit(() -> {
            System.out.println("执行任务: " + taskIndex + " on thread " + Thread.currentThread());
            Thread.sleep(Duration.ofSeconds(1)); // 模拟 I/O 阻塞
            return taskIndex;
        });
    }
} // try-with-resources 会自动关闭 executor
```

上面的代码可以瞬间创建 10 万个任务（即 10 万个虚拟线程），它们会并发执行，而底层的平台线程可能只有几个。如果用传统线程池，早就因为资源耗尽而崩溃了。

#### 适用场景与注意事项

- **最佳适用场景**：**I/O 密集型 (I/O-bound)** 的任务。例如，Web 应用、微服务、数据库访问、消息队列消费等，这些任务大部分时间都在等待数据返回。
    
- **不适用场景**：**CPU 密集型 (CPU-bound)** 的任务。例如，复杂的数学计算、视频编码等。对于这类任务，线程数应该与 CPU 核心数匹配，使用传统平台线程池是更合适的选择。
    
- **注意事项**：避免在虚拟线程中使用 `synchronized` 关键字锁定并执行阻塞 I/O 操作。这会导致虚拟线程被“钉”在载体线程上，使载体线程也跟着一起阻塞，从而破坏虚拟线程的性能优势。推荐使用 `java.util.concurrent.locks.ReentrantLock` 作为替代。
### Scoped Values（范围值）
好的，我们来详细解释一下 Java 的另一个重要新特性：**Scoped Values（范围值）**。

这个特性同样与 **Project Loom** 和**虚拟线程**密切相关，并在 Java 21 (LTS) 中最终定稿。它的主要目标是提供一种全新的、更安全、更高效的方式来在线程内部以及父子线程之间共享数据，旨在**取代**问题多多的传统 `ThreadLocal` 变量。

---

#### 一、 “旧时代”的 `ThreadLocal` 及其问题

在 Scoped Values 出现之前，如果想在同一个线程的处理流程中（例如，一个完整的 HTTP 请求处理链路）共享数据，而又不想通过方法参数层层传递，唯一的标准方式就是使用 `ThreadLocal`。

`ThreadLocal` 会为每个线程创建一个独立的变量副本。比如，你可以把用户信息存入 `ThreadLocal`，这样在这个线程的任何地方都能获取到当前用户信息。

**但 `ThreadLocal` 在现代高并发（尤其是虚拟线程）场景下，暴露了几个严重的设计缺陷：**

1. **可变性 (Mutability)**：`ThreadLocal` 里的值是**可变的**。链路上的任何代码都可以随时调用 `.set()` 方法来修改它。这使得数据流向变得难以追踪，很容易引入 Bug，一个模块不小心修改了值，可能会让另一个模块崩溃。
    
2. **昂贵的继承 (`InheritableThreadLocal`)**：如果希望父线程创建的子线程能继承 `ThreadLocal` 的值，需要使用 `InheritableThreadLocal`。它的实现方式是在创建子线程时，**拷贝**父线程的所有 `ThreadLocal` 值。在可以创建**上百万个虚拟线程**的今天，这种拷贝的成本是完全无法接受的。
    
3. **内存泄漏风险**：`ThreadLocal` 的生命周期与线程本身绑定。尤其是在使用传统线程池时，如果一个请求处理完后**忘记调用 `.remove()` 方法清理 `ThreadLocal`**，那么这个线程被下一个请求复用时，就会读到上一个请求的“脏数据”。这是非常常见且难以排查的 Bug。
    
4. **作用域不明确**：`ThreadLocal` 的值一旦被设置，在线程的整个生命周期内都有效，除非被手动移除。它的作用范围是“无边界”的，不清晰。
    

---

#### 二、 “新时代”的 Scoped Values

Scoped Values 的设计哲学就是为了解决上述所有问题。

**核心理念**：提供一种在一段**有限的代码范围内 (Scope)** 共享一个**不可变 (Immutable)** 数据的方式。

我们用一个“会议通行证”的比喻来理解：

- **`ThreadLocal`**：就像一个**挂在你脖子上的可擦写白板**。在会议期间，任何人都可以随时在上面写写画画（可变），你离开时如果忘了擦干净（忘记 remove），下一个戴这个牌子的人就会看到你的笔记（数据泄漏）。
    
- **`ScopedValue`**：就像你在进入某个**特定会议室（一个代码范围 Scope）时，门口发给你的一张打印好的、塑封的通行证**。在这个会议室里，任何人都可以**看**你的通行证（读取），但**绝对无法修改**它（不可变）。当你离开这个会议室时，通行证自动被收回（自动清理）。
    

---

#### 三、如何使用 Scoped Values

Scoped Values 的 API 非常简洁，核心是 `ScopedValue.where(...).run(...)` 这个模式。

**代码示例：** 我们来看一个经典的 Web 服务器场景，需要在处理请求期间共享用户信息。

**1. 定义一个 `ScopedValue`** 它通常被定义为一个 `public static final` 字段。

Java

```java
public class Context {
    // 定义一个 ScopedValue，它将用于携带 User 对象
    public static final ScopedValue<User> LOGGED_IN_USER = ScopedValue.newInstance();
}
```

**2. 在代码范围内“绑定”值并运行代码**

Java

```java
// 模拟 Web 框架的入口
public void handleRequest(Request request, Response response) {
    User currentUser = authenticateUser(request); // 获取当前用户

    // 使用 where 绑定值，然后用 run 执行代码块
    // 在这个 run 方法的范围内，LOGGED_IN_USER.get() 都是有效的
    ScopedValue.where(Context.LOGGED_IN_USER, currentUser)
               .run(() -> {
                   // === 进入了 Scoped Value 的作用域 ===

                   // 调用业务逻辑，我们不需要再传递 User 对象
                   new OrderService().processOrder();

                   // === 离开作用域，绑定自动失效 ===
               });
}

// 业务逻辑深处的某个类
public class OrderService {
    public void processOrder() {
        // 直接通过 isBound() 检查并 get() 获取值
        if (Context.LOGGED_IN_USER.isBound()) {
            User user = Context.LOGGED_IN_USER.get();
            System.out.println("正在为用户 " + user.getName() + " 处理订单...");
            // ... 业务逻辑 ...
            new PaymentService().charge();
        }
    }
}

// 支付服务，更深一层
public class PaymentService {
    public void charge() {
        // 在这里同样可以获取到 User 对象
        User user = Context.LOGGED_IN_USER.get();
        System.out.println("正在向用户 " + user.getName() + " 收费...");
    }
}
```

**这个模式的关键点：**

- **`where(key, value)`**: 指定要绑定哪个 `ScopedValue` 和要绑定的具体值。这个操作**不会立即执行**，而是返回一个 `Carrier`（携带者）对象。
    
- **`.run(runnable)`**: 传入一个 `Runnable`，这个 Lambda 表达式内的所有代码，就是该 Scoped Value 生效的“范围”。
    
- **自动清理**: 一旦 `.run()` 方法执行结束（无论是正常结束还是抛出异常），`LOGGED_IN_USER` 与 `currentUser` 的绑定关系就**自动解除**了。完全不需要手动清理！
    

---

#### 四、Scoped Values 的核心优势

1. **不可变性 (Immutability)** 在一个作用域内，`ScopedValue` 的值只能在入口处**绑定一次**，之后无法被任何代码修改。这使得数据流清晰可控，极大地提升了程序的健壮性。
    
2. **清晰且有限的作用域 (Clear and Bounded Scope)** 值的生命周期与 `run` 方法的代码块完全绑定，代码结构本身就清晰地定义了数据的作用范围。
    
3. **高效的继承与共享 (Efficient Sharing)** Scoped Values 是为虚拟线程量身定做的。当你在一个 `run` 的作用域内创建新的**子虚拟线程**时，子线程可以**极其高效地、零成本地继承**父线程的所有范围值。它避免了 `InheritableThreadLocal` 昂贵的拷贝开销，是虚拟线程环境下共享数据的最佳实践。
    
4. **杜绝内存泄漏 (Leak-Proof)** 由于其自动清理机制，彻底解决了 `ThreadLocal` 令人头疼的内存泄漏和数据污染问题。
    

#### 总结

**Scoped Values** 是对 Java 线程本地化数据共享机制的一次现代化重构。它通过强制**不可变性**和**结构化的作用域**，解决了 `ThreadLocal` 长期存在的各种问题，为编写健壮、高效、易于理解的高并发代码提供了强有力的支持。

在拥抱虚拟线程的时代，**使用 Scoped Values 替代 `ThreadLocal`** 将成为新的标准和最佳实践。
## 序列化

### 怎么把一个对象从一个jvm转移到另一个jvm?

- **使用序列化和反序列化** ：将对象序列化为字节流，并将其发送到另一个 JVM，然后在另一个 JVM 中反序列化字节流恢复对象。这可以通过 Java 的 ObjectOutputStream 和 ObjectInputStream 来实现。
- **使用消息传递机制** ：利用消息传递机制，比如使用消息队列（如 RabbitMQ、Kafka）或者通过网络套接字进行通信，将对象从一个 JVM 发送到另一个。这需要自定义协议来序列化对象并在另一个 JVM 中反序列化。
- **使用远程方法调用（RPC）** ：可以使用远程方法调用框架，如 gRPC，来实现对象在不同 JVM 之间的传输。远程方法调用可以让你在分布式系统中调用远程 JVM 上的对象的方法。
- **使用共享数据库或缓存** ：将对象存储在共享数据库（如 MySQL、PostgreSQL）或共享缓存（如 Redis）中，让不同的 JVM 可以访问这些共享数据。这种方法适用于需要共享数据但不需要直接传输对象的场景。

### 序列化和反序列化让你自己实现你会怎么做?

使用Java 默认的序列化
优点：简单
缺点：
- **无法跨语言**： Java 序列化目前只适用基于 Java 语言实现的框架
- **容易被攻击**：Java 序列化是不安全的，对象是通过在 ObjectInputStream 上调用 readObject() 方法进行反序列化的，但它同时可以将类路径上所有实现了 Serializable 接口的对象都实例化。这也就意味着，在反序列化字节流的过程中，该方法可以执行任意类型的代码，这是非常危险的。
- **序列化后的流太大**：序列化后的二进制流大小能体现序列化的性能。序列化后的二进制数组越大，占用的存储空间就越多，存储硬件的成本就越高。如果我们是进行网络传输，则占用的带宽就更多，这时就会影响到系统的吞吐量。

我会考虑用主流序列化框架，比如FastJson、Protobuf来替代Java 序列化。
#### Protobuf
创建一个名为 `user_profile.proto` 的文件，用来定义我们的 `User` 数据结构。
这个命令会读取 `user_profile.proto` 文件，并根据我们指定的 `java_package` 选项，在当前目录下生成一个 Java 文件：`com/example/models/UserProfileProto.java`
这个 `UserProfileProto.java` 文件就是 Protobuf 的魔法所在。它包含了：

- 一个外部类 `UserProfileProto`。
    
- 一个内部类 `User`，对应我们定义的 `message User`。
    
- 一个 `User.Builder` 类，用于创建和设置 `User` 对象。
    
- 所有字段的 getters 和 setters。
    
- **序列化** (`toByteArray()`) 和**反序列化** (`parseFrom()`) 的方法。

然后用`UserProfileProto.java` 这个文件对服务端和客户端进行加密和解密

### 将对象转为二进制字节流具体怎么实现?

其实，像序列化和反序列化，无论这些可逆操作是什么机制，都会有对应的 **处理和解析协议** ，例如加密和解密，TCP的粘包和拆包，序列化机制是通过序列化协议来进行处理的，和 class 文件类似，它其实是定义了序列化后的字节流格式，然后对此格式进行操作，生成符合格式的字节流或者将字节流解析成对象。
**字节码本质上是一种二进制码，但它是一种非常特殊的、非本地（non-native）的二进制码。**
在Java中通过序列化对象流来完成序列化和反序列化：

- ObjectOutputStream：通过writeObject(）方法做序列化操作。
- ObjectInputStrean：通过readObject()方法做反序列化操作。

实现对象序列化：

- 让类实现Serializable接口：
```java
import java.io.Serializable;

public class MyClass implements Serializable {
    // class code
}
```
- 创建输出流并写入对象：
```java
import java.io.FileOutputStream;
import java.io.ObjectOutputStream;

MyClass obj = new MyClass();
try {
    FileOutputStream fileOut = new FileOutputStream("object.ser");
    ObjectOutputStream out = new ObjectOutputStream(fileOut);
    out.writeObject(obj);
    out.close();
    fileOut.close();
} catch (IOException e) {
    e.printStackTrace();
}
```

实现对象反序列化：

- 创建输入流并读取对象：
```java
import java.io.FileInputStream;
import java.io.ObjectInputStream;

MyClass newObj = null;
try {
    FileInputStream fileIn = new FileInputStream("object.ser");
    ObjectInputStream in = new ObjectInputStream(fileIn);
    newObj = (MyClass) in.readObject();
    in.close();
    fileIn.close();
} catch (IOException | ClassNotFoundException e) {
    e.printStackTrace();
}
```

要确保类实现了Serializable或Externalizable接口，并且所有成员变量都是Serializable的才能被正确序列化。否则抛出异常

## I/O
### 什么是java的网络IO高并发编程？
使用 Java 技术栈来构建能够**同时处理成千上万甚至上百万个网络连接**的能力和相关的技术模型
**操作系统 (Operating System)** 在其中扮演了至关重要的**中介**角色。
**I/O 操作（尤其是网络 I/O）是缓慢且不可预测的，而 CPU 资源是宝贵的**。如何在高并发场景下，不让大量的线程因为等待缓慢的 I/O 而白白浪费掉宝贵的系统资源，这就是 Java 网络 I/O 模型不断演进的根本原因

BIO->NIO->AIO->虚拟线程
#### 1. 文件 I/O (File I/O)

- **双方是谁**：你的**应用程序进程** vs. **文件系统** (最终对应物理的硬盘或固态硬盘)。
    
- **操作**：
    
    - **Input**: 应用程序从文件中读取数据到内存。
        
    - **Output**: 应用程序将内存中的数据写入到文件。
        

#### 2. 网络 I/O (Network I/O)

- **双方是谁**：你服务器上的**应用程序进程** vs. 另一台计算机上的**远程应用程序进程**。
    
- **操作**：
    
    - **Input**: 你的应用程序从网络套接字 (Socket) 中读取远程进程发来的数据。
        
    - **Output**: 你的应用程序向网络套接字 (Socket) 中写入数据，发送给远程进程。
        

#### 3. 控制台 I/O (Console I/O)

- **双方是谁**：你的**应用程序进程** vs. **人类用户**。
    
- **操作**：
    
    - **Input**: 应用程序从标准输入 (`System.in`) 读取用户通过**键盘**输入的数据。
        
    - **Output**: 应用程序向标准输出 (`System.out`) 写入数据，最终显示在用户的**屏幕**上。
        

#### 4. 数据库 I/O (Database I/O)

- **双方是谁**：你的**应用程序进程** vs. **数据库服务进程** (例如 MySQL Server)。
    
- **操作**：这也是一种特殊的网络 I/O。
    
    - **Input**: 应用程序从数据库连接中读取查询结果。
        
    - **Output**: 应用程序通过数据库连接发送 SQL 查询语句。
#### 总结

| I/O 模型   | 编程模型  | 核心思想     | 优点            | 缺点          |
| -------- | ----- | -------- | ------------- | ----------- |
| **BIO**  | 同步阻塞  | 一个连接一个线程 | 简单直观          | 伸缩性差，无法高并发  |
| **NIO**  | 同步非阻塞 | I/O 多路复用 | **伸缩性极高**     | **编程模型复杂**  |
| **AIO**  | 异步非阻塞 | 事件回调     | 真异步           | 应用不广，编程复杂   |
| **虚拟线程** | 同步阻塞  | 轻量级线程    | **伸缩性高且编程简单** | 不适合CPU密集型任务 |
- **同步 (Synchronous) vs. 异步 (Asynchronous)**
    
    - 这个维度的核心在于：**由谁来负责检查 I/O 操作是否完成**。
        
    - **同步**：**应用程序自己**负责。你的代码发起 I/O 请求后，必须通过某种方式（阻塞等待或者不断轮询）来主动检查操作是否就绪或完成。
        
    - **异步**：**操作系统 (Kernel)** 负责。你的代码发起 I/O 请求后就立刻返回，当操作完成后，由操作系统来**通知**你的应用程序（例如，通过调用你预先注册的回调函数）。
        
- **阻塞 (Blocking) vs. 非阻塞 (Non-blocking)**
    
    - 这个维度的核心在于：**发起 I/O 请求的线程会不会被挂起**。
        
    - **阻塞**：当线程发起一个 I/O 操作（如 `read()`) 时，如果数据还没准备好，这个线程就会被**挂起（睡眠）**，直到数据准备好为止。
        
    - **非阻塞**：当线程发起一个 I/O 操作时，无论数据是否准备好，调用都会**立即返回**。如果没准备好，它可能会返回一个特殊的值（例如 0），然后你的代码需要决定下一步做什么（比如过会儿再试）。

### Java怎么实现网络IO高并发编程？

可以用 Java NIO ，是一种同步非阻塞的I/O模型，也是I/O多路复用的基础。

传统的BIO里面socket.read()，如果TCP RecvBuffer里没有数据，函数会一直阻塞，直到收到数据，返回读到的数据， 如果使用BIO要想要并发处理多个客户端的i/o，那么会使用多线程模式，一个线程专门处理一个客户端 io，这种模式随着客户端越来越多，所需要创建的线程也越来越多，会急剧消耗系统的性能。

![image-20240820112641716](https://cdn.xiaolincoding.com//picgo/image-20240820112641716.png)

NIO 是基于I/O多路复用实现的，它可以只用一个线程处理多个客户端I/O，如果你需要同时管理成千上万的连接，但是每个连接只发送少量数据，例如一个聊天服务器，用NIO实现会更好一些。

![image-20240820112656259](https://cdn.xiaolincoding.com//picgo/image-20240820112656259.png)

### BIO、NIO、AIO区别是什么？

- BIO（blocking IO）：就是传统的 java.io 包，它是基于流模型实现的，交互的方式是同步、阻塞方式，也就是说在读入输入流或者输出流时，在读写动作完成之前，线程会一直阻塞在那里，它们之间的调用是可靠的线性顺序。优点是代码比较简单、直观；缺点是 IO 的效率和扩展性很低，容易成为应用性能瓶颈。
- NIO（non-blocking IO） ：Java 1.4 引入的 java.nio 包，提供了 Channel、Selector、Buffer 等新的抽象，可以构建多路复用的、同步非阻塞 IO 程序，同时提供了更接近操作系统底层高性能的数据操作方式。
- AIO（Asynchronous IO） ：是 Java 1.7 之后引入的包，是 NIO 的升级版本，提供了异步非堵塞的 IO 操作方式，所以人们叫它 AIO（Asynchronous IO），异步 IO 是基于事件和回调机制实现的，也就是应用操作之后会直接返回，不会堵塞在那里，当后台处理完成，操作系统会通知相应的线程进行后续的操作。

### NIO是怎么实现的？

NIO是一种同步非阻塞的IO模型，所以也可以叫NON-BLOCKINGIO。同步是指线程不断轮询IO事件是否就绪，非阻塞是指线程在等待IO的时候，可以同时做其他任务。

同步的核心就Selector（I/O多路复用），Selector代替了线程本身轮询IO事件，避免了阻塞同时减少了不必要的线程消耗；非阻塞的核心就是通道和缓冲区，当IO事件就绪时，可以通过写到缓冲区，保证IO的成功，而无需线程阻塞式地等待。

NIO由一个专门的线程处理所有IO事件，并负责分发。**事件驱动机制**，事件到来的时候触发操作，不需要阻塞的监视事件。**线程之间通过wait,notify通信**，减少线程切换。

NIO主要有三大核心部分：Channel(通道)，Buffer(缓冲区), Selector。**传统IO基于字节流和字符流进行操作，而NIO基于Channel和Buffer(缓冲区)进行操作，数据总是从通道读取到缓冲区中，或者从缓冲区写入到通道中。**

Selector(选择区)用于监听多个通道的事件（比如：连接打开，数据到达）。因此，单个线程可以监听多个数据通道。
更准确地说，Selector 应该被理解为一个**对象**、一个**工具**，或者一个**中介**。而**线程 (Thread)** 才是那个**使用**这个工具的**主动执行者**。
NIO 通过引入 Channel、Buffer 和 Selector 三大组件，构建了一套 I/O 多路复用的、同步非阻塞的事件驱动模型。其核心在于，允许单个线程通过阻塞在 Selector 上来高效地监控和管理成千上万个非阻塞的 Channel。当任意 Channel 上的 I/O 事件就绪时，Selector 会唤醒该线程，线程则根据事件类型，通过 Buffer 对数据进行处理，从而以极少的线程资源实现超高的并发连接处理能力。

![img](https://cdn.xiaolincoding.com//picgo/1716018476312-e5525ca7-acf8-46b1-8fff-8a7d22db5304.webp)

### 你知道有哪个框架用到NIO了吗？

**Netty。**
#### 一、 Netty 解决了什么核心问题？

我们之前讨论过，虽然 NIO 性能极高，但直接使用它来编程是一场噩梦。开发者需要处理：

1. **API 复杂性**：手动管理 `Buffer` 的 `flip()`, `clear()` 等状态，非常繁琐且容易出错。
    
2. **CPU 空转 Bug**：需要非常小心地处理 `OP_READ` 事件的注册与取消，否则容易导致 `Selector` 空轮询，CPU 占用 100%。
    
3. **TCP “半包/粘包”问题**：TCP 是流式协议，数据包可能被拆分或合并。NIO 本身不处理这个问题，需要开发者自己解析数据流，非常复杂。
    
4. **连接管理和状态跟踪**：需要手动管理所有 `SelectionKey` 的状态，处理连接的断开、异常等。
    
5. **空洞的协议支持**：NIO 只提供了基础的 TCP/UDP 传输能力，如果要实现 HTTP、WebSocket 等上层协议，需要自己编写大量的编解码代码。
    

**Netty 作为一个框架，完美地解决了以上所有问题。** 它对 NIO 进行了深度封装和优化，提供了一套更高级、更易用的 API。

---

#### 二、 Netty 的核心架构组件

Netty 的强大之处在于其优雅、模块化的架构设计。理解了下面几个核心组件，就理解了 Netty 的工作方式。

##### 1. `EventLoop` & `EventLoopGroup` (事件循环与事件循环组)

这是 Netty 的**并发模型和“引擎”**。

- `EventLoop` 是一个**死循环**，在其生命周期内，它不断地检查是否有新的 I/O 事件，并处理它们。**一个 `EventLoop` 通常只由一个线程驱动**，这避免了多线程并发问题。
    
- `EventLoop` 内部就封装了我们之前讨论的 Java NIO `Selector`。
    
- `EventLoopGroup` 是一组 `EventLoop` 的集合，可以看作是一个**线程池**。
    

Netty 最经典的并发模型是**“主从 Reactor 模式”**：

- **Boss Group (老板/主循环组)**：通常只包含 **1 个 `EventLoop`**（即 1 个线程）。它的唯一职责就是监听服务器端口，**接受新的客户端连接 (`accept` 事件)**，然后将建立好的连接**交给 Worker Group**。
    
- **Worker Group (工人/从循环组)**：通常包含**多个 `EventLoop`**（线程数一般是 CPU 核心数的 2 倍）。它负责处理所有已建立连接的**读写事件 (`read`, `write` 事件)** 和业务逻辑。
    

这种“职责分离”的模式使得连接的接受和数据的读写互不干扰，性能极高。

##### 2. `Channel` (通道)

这是 Netty 对网络连接的抽象，可以看作是 Java NIO `Channel` 的增强版。它代表了一个到实体（如硬件设备、文件、网络套接字）的开放连接，能够进行 I/O 操作。

##### 3. `ChannelPipeline` & `ChannelHandler` (通道流水线与处理器)

这是 Netty **最核心、最精妙**的设计，也是开发者主要打交道的地方。

- **`ChannelPipeline`**：
    
    - 每个 `Channel` 都拥有一个自己的 `ChannelPipeline`。
        
    - 它可以被看作一条**流水线**，上面流动着入站（Inbound）和出站（Outbound）的 I/O 事件。
        
- **`ChannelHandler`**：
    
    - 就是流水线上的一个个**处理站**。你通过将多个 `Handler` 添加到 `Pipeline` 中，来构建你的处理逻辑。
        
    - **`ChannelInboundHandler` (入站处理器)**：处理**入站**事件，通常是**读取**客户端数据、解码、执行业务逻辑等。事件从 `Pipeline` 的头部流向尾部。
        
    - **`ChannelOutboundHandler` (出站处理器)**：处理**出站**事件，通常是**写入**数据到客户端、编码等。事件从 `Pipeline` 的尾部流向头部。
        

**这个设计的巨大优势**：

- **高度解耦**：每个 `Handler` 只关心自己的逻辑。例如，你可以有一个专门负责解码的 `Handler`，一个负责编码的 `Handler`，一个负责处理心跳的 `Handler`，一个负责执行核心业务的 `Handler`。
    
- **逻辑清晰，可复用**：整个数据处理流程被分解成一系列清晰的步骤，非常易于维护和复用。
    

##### 4. `ByteBuf` (字节缓冲区)

这是 Netty 对 Java NIO `ByteBuffer` 的重大改进，解决了其所有痛点。

- **无需 `flip()`**：`ByteBuf` 内部维护了**两个独立的指针**：`readerIndex` (读指针) 和 `writerIndex` (写指针)，使得读写切换不再需要调用 `flip()`，极大简化了操作。
    
- **零拷贝 (Zero-Copy)**：提供了多种机制，可以在不进行内存复制的情况下，高效地对数据进行切片、组合等操作。
    
- **池化 (Pooling)**：内置了高性能的内存池，可以重用 `ByteBuf` 对象，避免了频繁创建和销毁对象带来的 GC 压力。
    
- **自动扩容**：当写入数据超过容量时，`ByteBuf` 会自动扩容，非常方便。

**池化 (Pooling)** 是一种非常重要的软件设计模式和性能优化技术。其核心思想是：**对于那些创建成本高昂或数量有限的资源，预先创建并维护一个“资源池” (Pool)，当需要使用资源时，从池中借用；使用完毕后，再将其归还到池中，以供后续重复使用。**

简单来说，池化的精髓就是 **“复用代替创建”**
##### 5. `Future` & `Promise`

Netty 中所有的 I/O 操作都是**异步**的。当你调用一个 `write()` 方法时，它会**立即返回**一个 `ChannelFuture` 对象，而不会等待操作真正完成。

- **`ChannelFuture`**：你可以给这个 `Future` 对象添加一个监听器 (`listener`)。当 I/O 操作最终完成时（无论成功还是失败），这个监听器就会被**回调**。
    
- 这种机制让你的线程不必等待 I/O，可以立刻去处理其他任务，是实现高吞吐量的关键。

**Netty 框架内部与 `Selector` 交互**。开发者完全看不到 `Selector`，只与 `Channel`, `Pipeline`, `Future` 等高级抽象交互。

---

#### Netty 服务器的工作流程（简化版）

Java

```
// 1. 创建 Boss 和 Worker 两个 EventLoopGroup
EventLoopGroup bossGroup = new NioEventLoopGroup(1);
EventLoopGroup workerGroup = new NioEventLoopGroup();

try {
    // 2. 创建服务器启动引导类 ServerBootstrap
    ServerBootstrap b = new ServerBootstrap();
    b.group(bossGroup, workerGroup) // 3. 配置 Boss 和 Worker 组
     .channel(NioServerSocketChannel.class) // 4. 指定使用 NIO 的 Channel
     .childHandler(new ChannelInitializer<SocketChannel>() { // 5. 设置 Worker 组的处理逻辑
         @Override
         public void initChannel(SocketChannel ch) throws Exception {
             // 6. 获取 Pipeline，并添加多个 Handler
             ChannelPipeline p = ch.pipeline();
             p.addLast(new MyDecoder()); // 添加解码器
             p.addLast(new MyEncoder()); // 添加编码器
             p.addLast(new MyBusinessLogicHandler()); // 添加业务处理器
         }
     });

    // 7. 绑定端口，启动服务器 (这是一个异步操作)
    ChannelFuture f = b.bind(8080).sync();
    
    // 等待服务器关闭
    f.channel().closeFuture().sync();
} finally {
    // 优雅地关闭
    workerGroup.shutdownGracefully();
    bossGroup.shutdownGracefully();
}
```

#### 总结

**Netty 是一个建立在 Java NIO 之上的高级框架，它通过提供一套精心设计的、易于使用的抽象（如 `EventLoop`, `Pipeline`, `ByteBuf`），将开发者从 NIO 复杂的底层细节中解放出来。**

它为你处理了所有网络编程中的脏活累活（事件循环、并发控制、半包粘包、编解码等），让你能够像搭建乐高一样，通过组合不同的 `Handler` 来快速、安全地构建出极其稳定和高性能的网络应用。几乎所有知名的 Java 开源项目（如 Dubbo, gRPC, Elasticsearch, Flink 等）的网络层都使用了 Netty
Netty 的 I/O 模型是基于非阻塞 I/O 实现的，底层依赖的是 NIO 框架的多路复用器 Selector。采用 epoll 模式后，只需要一个线程负责 Selector 的轮询。当有数据处于就绪状态后，需要一个事件分发器（Event Dispather），它负责将读写事件分发给对应的读写事件处理器（Event Handler）。事件分发器有两种设计模式：Reactor 和 Proactor，Reactor 采用同步 I/O， Proactor 采用异步 I/O。

![img](https://cdn.xiaolincoding.com//picgo/1715424254674-7a7159b1-d1ed-4236-ae18-09421c9837ed.png)

Reactor 实现相对简单，适合处理耗时短的场景，对于耗时长的 I/O 操作容易造成阻塞。Proactor 性能更高，但是实现逻辑非常复杂，适合图片或视频流分析服务器，目前主流的事件驱动模型还是依赖 select 或 epoll 来实现。

## 其他

### 有一个学生类，想按照分数排序，再按学号排序，应该怎么做？

可以使用Comparable接口来实现按照分数排序，再按照学号排序。首先在学生类中实现Comparable接口，并重写compareTo方法，然后在compareTo方法中实现按照分数排序和按照学号排序的逻辑。

```java
public class Student implements Comparable<Student> {
    private int id;
    private int score;

    // 构造方法和其他属性、方法省略

    @Override
    public int compareTo(Student other) {
        if (this.score != other.score) {
            return Integer.compare(other.score, this.score); // 按照分数降序排序
        } else {
            return Integer.compare(this.id, other.id); // 如果分数相同，则按照学号升序排序
        }
    }
}
```

然后在需要对学生列表进行排序的地方，使用Collections.sort()方法对学生列表进行排序即可：

```
List<Student> students = new ArrayList<>();
// 添加学生对象到列表中
Collections.sort(students);
```

### 对象的比较

#### 1. `Comparable<T>` 接口 (内部比较器 / 自然顺序)

- **原理**：让一个类自己实现 `Comparable` 接口，意味着这个类的对象天生就**具有了“可比较性”**，这被称为**自然顺序 (Natural Ordering)**。
    
- **核心方法**：`int compareTo(T other)`
    
- **返回值约定**：
    
    - 返回**负整数**：表示 `this` 对象小于 `other` 对象。
        
    - 返回**零**：表示 `this` 对象等于 `other` 对象。
        
    - 返回**正整数**：表示 `this` 对象大于 `other` 对象。
        
- **适用场景**：当一个类有非常明确、唯一的排序规则时（例如，`Integer` 按数值大小，`String` 按字典顺序）。
    

**示例（让 `Person` 按年龄排序）：**

Java

```
public class Person implements Comparable<Person> {
    // ... name 和 age 字段 ...

    @Override
    public int compareTo(Person other) {
        // 按照 age 升序排序
        return Integer.compare(this.age, other.age);
        // 如果 this.age < other.age, 返回负数
        // 如果 this.age == other.age, 返回 0
        // 如果 this.age > other.age, 返回正数
    }
}
```

#### 2. `Comparator<T>` 接口 (外部比较器 / 定制顺序)

- **原理**：创建一个**独立的类**来实现 `Comparator` 接口，用于定义一种**特定的、外部的**比较规则。
    
- **核心方法**：`int compare(T o1, T o2)`
    
- **返回值约定**：与 `compareTo` 类似。
    
- **适用场景**：
    
    - 当一个类没有实现 `Comparable`，但你又想对它进行排序。
        
    - 当一个类需要**多种不同的排序方式**时（例如，`Person` 有时需要按年龄排序，有时需要按姓名排序）。
        
    - 当你无法修改类的源代码时。
        

**示例（创建一个按姓名排序的比较器）：**

Java

```
import java.util.Comparator;

public class PersonNameComparator implements Comparator<Person> {
    @Override
    public int compare(Person p1, Person p2) {
        // 按照 name 的字典顺序排序
        return p1.getName().compareTo(p2.getName());
    }
}
```

**在 Java 8+ 中，使用 Lambda 表达式和 `Comparator` 的静态辅助方法会更简洁：**

Java

```
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

// ...
List<Person> people = new ArrayList<>();
// ... add people ...

// 使用 Lambda 表达式按姓名排序
people.sort((p1, p2) -> p1.getName().compareTo(p2.getName()));

// 使用 Comparator.comparing 静态方法，更简洁、更优雅！
people.sort(Comparator.comparing(Person::getName));

// 甚至可以实现更复杂的排序，比如先按年龄排，再按姓名排
people.sort(Comparator.comparing(Person::getAge)
                      .thenComparing(Person::getName));
```
### Native方法解释一下

在Java中，native方法是一种特殊类型的方法，它允许Java代码调用外部的本地代码，即用C、C++或其他语言编写的代码。native关键字是Java语言中的一种声明，用于标记一个方法的实现将在外部定义。

在Java类中，native方法看起来与其他方法相似，只是其方法体由**native关键字**代替，没有实际的实现代码。例如：

```java
public class NativeExample {
    public native void nativeMethod();
}
```

要实现native方法，你需要完成以下步骤：

1. **生成JNI头文件** ：使用javah工具从你的Java类生成C/C++的头文件，这个头文件包含了所有native方法的原型。
2. **编写本地代码** ：使用C/C++编写本地方法的实现，并确保方法签名与生成的头文件中的原型匹配。
3. **编译本地代码** ：将C/C++代码编译成动态链接库（DLL，在Windows上），共享库（SO，在Linux上）
4. **加载本地库** ：在Java程序中，使用System.loadLibrary()方法来加载你编译好的本地库，这样JVM就能找到并调用native方法的实现了。
### 水平触发和边缘触发
#### 1. 水平触发 (Level-Triggered, LT)

这是 `select`、`poll` 以及 `epoll` 的**默认工作模式**，也是 **Java NIO `Selector`** 的行为模式。

- **定义**：只要文件描述符（Channel）处于某个你感兴趣的状态（例如，可读或可写），`select()` 调用就会**持续地返回**，通知你这个事件。
    
- **对于读事件 (`OP_READ`)**：
    
    - **条件**：只要操作系统的 Socket 接收缓冲区中**有数据**。
        
    - **行为**：`selector.select()` 就会被唤醒。如果你这次只读取了缓冲区的一部分数据，缓冲区里**仍然还有数据**，那么在下一次循环中调用 `select()` 时，它会**立刻再次返回**，继续通知你这个 Channel 是可读的。
        
- **编程视角**：
    
    - **优点**：编程相对简单，容错性好。即使你这次因为某种原因没有处理完所有数据，没关系，下一次循环 `Selector` 还会“唠叨”你，提醒你去处理。你**不容易丢失事件**。
        
    - **缺点**：可能导致**惊群效应**和**CPU 100% 空转**。正如我们之前讨论的，如果你的应用程序 Buffer 满了，导致你无法从 Socket 缓冲区读取数据，LT 模式会不断地、徒劳地唤醒你的线程，造成 CPU 资源浪费。
        

---

#### 2. 边缘触发 (Edge-Triggered, ET)

这是 `epoll` 特有的、更高性能的模式。高性能网络框架如 Netty 会使用它。

- **定义**：只有当文件描述符（Channel）的**状态发生变化**时，`select()` 才会返回一次，通知你这个事件。
    
- **对于读事件 (`OP_READ`)**：
    
    - **条件**：仅在 Socket 接收缓冲区的数据量**从 0 变为 >0 的那一瞬间**（或者有新数据追加进来时）。
        
    - **行为**：`selector.select()` 只会唤醒你**一次**。操作系统会假设你已经知道了这个事件，并且会处理它。如果你这次没有把缓冲区的数据全部读完，操作系统**不会再次**为这些“剩余”的数据通知你。它只会等到**下一次新的数据**到达时，才会再次触发通知。
        
- **编程视角**：
    
    - **优点**：效率更高。它极大地减少了 `select()` 被唤醒的次数，避免了 LT 模式下的空转问题。线程只在真正有新工作要做时才被唤醒。
        
    - **缺点**：编程复杂度**极高**，且非常容易出错。
        
        - **必须一次性读完**：当收到一个读事件通知时，你必须在一个非阻塞的循环中持续调用 `read()`，直到它返回 -1 (连接关闭) 或抛出 `EWOULDBLOCK` / `EAGAIN` 异常（表示数据已经读完了），否则就会有数据残留在缓冲区而你却永远不会再收到通知，导致连接“饿死”。
            
        - **事件可能丢失**：如果你处理不当，就相当于错过了唯一的通知，导致数据处理延迟或丢失。
            

---

#### 总结对比

|特性|水平触发 (Level-Triggered, LT)|边缘触发 (Edge-Triggered, ET)|
|---|---|---|
|**触发时机**|只要条件**满足**，就持续触发|仅在状态**发生变化**时，触发一次|
|**通知次数**|**多次**，直到条件消失|**仅一次**，在状态变化时|
|**编程复杂度**|**较低**，不易丢失事件|**较高**，必须一次性处理完|
|**潜在问题**|**CPU 空转** (Busy-Spin)|事件丢失，连接“饿死”|
|**性能**|较好|**更高**|
|**典型代表**|Java NIO `Selector` (默认行为)|Linux `epoll` 的 `EPOLLET` 模式 / Netty|

导出到 Google 表格
