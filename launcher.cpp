// For a master executable under Windows
// For Windows version, a wrapped single executable will be provided

# include <string>
// not <iostream> for smaller size

int main(int argc, char** argv) {
    system("start python.exe main.py");
    system("start http://localhost:8101/");
    return 0;
}
