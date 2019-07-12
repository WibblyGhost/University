.class public Program
.super java/lang/Object
.method public <init>()V
aload_0
invokenonvirtual java/lang/Object/<init>()V
return
.end method
.method public static main([Ljava/lang/String;)V
.limit locals 3
.limit stack 1024
new java/util/Scanner
dup
getstatic java/lang/System.in Ljava/io/InputStream;
invokespecial java/util/Scanner.<init>(Ljava/io/InputStream;)V
astore 0
sipush 0
istore 1
l1:
iload 2
sipush 0
if_icmple l2
iload 1
iload 2
iadd
istore 1
iload 2
sipush 1
isub
istore 2
goto l1
l2:
return
.end method
