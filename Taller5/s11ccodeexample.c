int proc (int a, int b, int c, int d) {
        int e,f;
        e = 2;
        f=a+b+c+d+e;
        return f;
}

/* entry point */
int main () {
        int a,b,c;
        a = 6;
        b = 5;
        c = proc (a, b, 8, 7);
        return c;
}