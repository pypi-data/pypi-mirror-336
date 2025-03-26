def all_operation():
    print("This is to Appling all operation on your two digit")

    a = int(input("Enter first value: "))
    b = int(input("Enter second value: "))

    print("Addition of both the numbers: ",a+b)
    print("Subtraction of both the number: ",a-b)
    print("Multiplication of both the number: ",a*b)
    print("Division of both the number: ",a/b)
    print("Floor Division of both the number: ",a//b)

print("")
print("")
print("")
print("")


def circumference_circle():
    print("This is to calculating area and circumference of a circle")

    r = int(input("Enter the radius of a circle: "))

    areaoc =3.14*r*r
    circumferenceoc = 2*3.14*r

    print("circumference of circle: ",circumferenceoc)
    print("Area of circle: ",areaoc)

print("")
print("")
print("")
print("")


def perimeter_of_square():
    print("This is to calculating area and perimeter of a square")

    s= int(input("Enter side of the square: "))

    areaos = s*s
    perimeterosq = 4*s

    print("Perimeter of square: ",perimeterosq)
    print("Area of square: ",areaos)

print("")
print("")
print("")
print("")




def perimeter_of_rectangle():

    print("This is to calculating area and perimeter of a rectangle")

    lor= int(input("Enter length of the rectangle: "))
    bor= int(input("Enter breath of the rectangle: "))

    areaorec = lor*bor
    perimeterorec = 2*(lor+bor)

    print("Area of rectangle: ",areaorec)
    print("Perimeter of rectangle: ",perimeterorec)

print("")
print("")
print("")
print("")


def area_of_triangle():

    print("This is to calculating area of a triangle")

    ht= int(input("Enter height of the triangle: "))
    bt= int(input("Enter base of the triangle: "))

    areaotria =1/2*bt*ht

    print("Area of triangle: ",areaotria)

print("")
print("")
print("")
print("")



def perimeter_of_triangle():

    print("This is to calculating perimeter of a triangle")

    sideone= int(input("Enter first side of the triangle: "))
    sidetwo= int(input("Enter second side of the triangle: "))
    sidethree= int(input("Enter thired side of the triangle: "))

    perimeter_of_triangle = sideone+sidetwo+sidethree

    print("perimeter of triangle: ",perimeter_of_triangle)

print("")
print("")
print("")
print("")



def calculating_simple_intrest():
    print("This is to calculating the simple intrest")

    pa= int(input("Enter principal amount: "))
    ti= int(input("Enter time: "))
    ra= int(input("Enter Rate: "))

    simint = pa*ti*ra/100
    tar = simint+pa

    print("Simple intrest: ",simint)
    print("Total amount to be return: ",tar)

print("")
print("")
print("")
print("")




def check_profit_or_loss():

    print("To check wheather loss or profit")

    cp= int(input("Enter cost price: "))
    sp= int(input("Enter selling price: "))

    if cp>sp:
        print("its loss")
    else:
        print("its profit")

print("")
print("")
print("")
print("")




def calculate_profit():

    print("To calculate profit")

    cdddwa= int(input("Enter selling price: "))
    cpaeer= int(input("Enter cost price: "))

    prwq= cdddwa-cpaeer

    print("Profit persentage: ",prwq)

print("")
print("")
print("")
print("")


def calculate_loss():

    print("To calculate loss")

    cddwa= int(input("Enter selling price: "))
    cpaer= int(input("Enter cost price: "))

    prw= cpaer-cddwa

    print("Profit persentage: ",prw)

print("")
print("")
print("")
print("")




def profit_persentage():
    print("To calculate profit persentage")

    prof= int(input("Enter profit: "))
    cpa= int(input("Enter cost price: "))

    profi= prof/cpa*100

    print("Profit persentage: ",profi)

print("")
print("")
print("")
print("")



def loss_persentage():

    print("To calculate loss persentage")

    los= int(input("Enter loss: "))
    c= int(input("Enter cost price: "))

    pro= los/c*100

    print("Profit persentage: ",pro)

print("")
print("")
print("")
print("")



def calculate_square_of_number():

    print("To calculate square of the number")

    f= int(input("Enter the number: "))

    g=f**2

    print("Square of the number is: ",g)

print("")
print("")
print("")
print("")



def calculate_cube_of_number():

    print("To calculate cube of the number")

    h= int(input("Enter the number: "))

    i=h**3

    print("Square of the number is: ",i)
