import customtkinter as ctk
import psutil
import threading
import time
import subprocess
import ctypes
from ctypes import wintypes
from tkinter import messagebox

# ===============================
# CONFIG INICIAL
# ===============================
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# ===============================
# ADMIN
# ===============================
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def executar(cmd):
    subprocess.run(cmd, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)

# ===============================
# LIMPAR RAM REAL
# ===============================
psapi = ctypes.WinDLL('psapi')
kernel32 = ctypes.WinDLL('kernel32')

EmptyWorkingSet = psapi.EmptyWorkingSet
EmptyWorkingSet.argtypes = [wintypes.HANDLE]
EmptyWorkingSet.restype = wintypes.BOOL

def limpar_memoria_ram():
    for proc in psutil.process_iter(['pid']):
        try:
            h = kernel32.OpenProcess(0x1F0FFF, False, proc.pid)
            if h:
                EmptyWorkingSet(h)
                kernel32.CloseHandle(h)
        except:
            pass

# ===============================
# APP
# ===============================
class PyOptiFlowApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("PyOptiFlow • Advanced System Optimizer")
        self.geometry("1280x780")
        self.resizable(False, False)
        self.attributes("-alpha", 0.95)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar()
        self.pages()
        self.show("dashboard")

        if not is_admin():
            messagebox.showwarning(
                "Administrador",
                "Execute como ADMINISTRADOR para otimizações reais."
            )

        threading.Thread(target=self.monitorar, daemon=True).start()

    # ===============================
    # SIDEBAR
    # ===============================
    def sidebar(self):
        self.menu = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.menu.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(
            self.menu,
            text="PyOptiFlow",
            font=("Segoe UI", 26, "bold"),
            text_color="#38bdf8"
        ).pack(pady=30)

        for nome, key in [
            ("Dashboard", "dashboard"),
            ("Otimização", "opt"),
            ("Limpeza", "clean"),
            ("🎮 Jogos", "games"),
            ("Configurações", "config"),
        ]:
            ctk.CTkButton(
                self.menu,
                text=nome,
                height=45,
                anchor="w",
                fg_color="transparent",
                hover_color="#1e293b",
                command=lambda k=key: self.show(k)
            ).pack(fill="x", padx=10, pady=6)

        ctk.CTkButton(
            self.menu,
            text="🔥 MODO TURBO",
            fg_color="#f97316",
            hover_color="#ea580c",
            height=45,
            command=self.modo_turbo
        ).pack(side="bottom", padx=10, pady=20)

    # ===============================
    # PAGES
    # ===============================
    def pages(self):
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        self.pg = {
            "dashboard": self.dashboard(),
            "opt": self.otimizacao(),
            "clean": self.limpeza(),
            "games": self.jogos(),
            "config": self.config()
        }

    def show(self, key):
        for p in self.pg.values():
            p.pack_forget()
        self.pg[key].pack(fill="both", expand=True)

    # ===============================
    # DASHBOARD
    # ===============================
    def dashboard(self):
        f = ctk.CTkFrame(self.container, fg_color="transparent")
        self.cpu = self.card(f, "CPU")
        self.ram = self.card(f, "RAM")
        self.disk = self.card(f, "DISCO")
        return f

    def card(self, parent, title):
        c = ctk.CTkFrame(parent, width=250, height=120)
        c.pack(side="left", padx=10, pady=10)
        ctk.CTkLabel(c, text=title, text_color="gray").pack(pady=(10, 0))
        lbl = ctk.CTkLabel(c, text="0%", font=("Segoe UI", 22, "bold"))
        lbl.pack(pady=10)
        return lbl

   # ===============================
    # CONFIRMAÇÃO
    # ===============================
def confirmar_otimizacao(self, titulo, descricao, comando):
    msg = (
        f"{titulo}\n\n"
        f"O que isso faz:\n{descricao}\n\n"
        "⚠️ Essa alteração afeta o sistema.\n"
        "Deseja realmente aplicar?"
    )

    if messagebox.askyesno("Confirmação de Otimização", msg):
        executar(comando)
        messagebox.showinfo("PyOptiFlow", "Otimização aplicada com sucesso!")

# ===============================
# OTIMIZAÇÃO — 25 OTIMIZAÇÕES REAIS (COM CONFIRMAÇÃO)
# ===============================
def otimizacao(self):
    f = ctk.CTkScrollableFrame(self.container)

    ctk.CTkLabel(
        f,
        text="🚀 25 Otimizações Reais de Sistema",
        font=("Segoe UI", 20, "bold")
    ).pack(anchor="w", pady=10)

    otim = [
        (
            "1 ⚡ Plano Alto Desempenho",
            "Ativa o plano de energia de máximo desempenho, evitando economia de CPU.",
            "powercfg /setactive SCHEME_MIN"
        ),
        (
            "2 🎮 Game Mode ON",
            "Ativa o Modo Jogo do Windows para priorizar jogos.",
            "reg add HKCU\\Software\\Microsoft\\GameBar /v AllowAutoGameMode /t REG_DWORD /d 1 /f"
        ),
        (
            "3 🚫 Xbox Game Bar OFF",
            "Desativa a Xbox Game Bar para reduzir consumo em jogos.",
            "reg add HKCU\\Software\\Microsoft\\GameBar /v ShowStartupPanel /t REG_DWORD /d 0 /f"
        ),
        (
            "4 🪟 Animações OFF",
            "Remove atrasos e animações da interface do Windows.",
            "reg add HKCU\\Control Panel\\Desktop /v MenuShowDelay /t REG_SZ /d 0 /f"
        ),
        (
            "5 🌐 TCP Low Latency",
            "Reduz latência de rede, ideal para jogos online.",
            "netsh int tcp set global autotuninglevel=disabled"
        ),
        (
            "6 📈 System Responsiveness 0",
            "Prioriza aplicações em tempo real (jogos).",
            "reg add HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile /v SystemResponsiveness /t REG_DWORD /d 0 /f"
        ),
        (
            "7 📡 Telemetria OFF",
            "Desativa coleta de dados do Windows.",
            "reg add HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection /v AllowTelemetry /t REG_DWORD /d 0 /f"
        ),
        (
            "8 🧠 CPU 100%",
            "Impede o Windows de limitar a CPU.",
            "powercfg -setacvalueindex SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX 100"
        ),
        (
            "9 🎯 GPU Priority Máxima",
            "Aumenta prioridade da GPU para jogos.",
            "reg add HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games /v GPU Priority /t REG_DWORD /d 8 /f"
        ),
        (
            "10 📦 TCP RSS ON",
            "Melhora desempenho de rede usando múltiplos núcleos.",
            "netsh int tcp set global rss=enabled"
        ),
        (
            "11 🧩 Desativar SysMain",
            "Desativa serviço que pode causar stutter em PCs fracos.",
            "sc stop SysMain & sc config SysMain start= disabled"
        ),
        (
            "12 🪫 Desativar Hibernação",
            "Libera espaço em disco e evita consumo extra.",
            "powercfg -h off"
        ),
        (
            "13 🔋 USB Power OFF",
            "Impede economia de energia nas portas USB.",
            "powercfg -setacvalueindex SCHEME_CURRENT SUB_USB USBSELECTIVE SUSPEND 0"
        ),
        (
            "14 🔥 Explorer Alta Prioridade",
            "Aumenta prioridade do explorer.exe.",
            "wmic process where name='explorer.exe' CALL setpriority 128"
        ),
        (
            "15 🧼 Limpar DNS",
            "Limpa cache de DNS para conexões mais estáveis.",
            "ipconfig /flushdns"
        ),
        (
            "16 🌍 TCP ECN OFF",
            "Desativa ECN para reduzir latência.",
            "netsh int tcp set global ecncapability=disabled"
        ),
        (
            "17 🧠 Prioridade Jogos",
            "Prioriza processos de jogos no sistema.",
            "reg add HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games /v Priority /t REG_DWORD /d 6 /f"
        ),
        (
            "18 🚀 Mouse Responsivo",
            "Remove aceleração e delays do mouse.",
            "reg add HKCU\\Control Panel\\Mouse /v MouseThreshold1 /t REG_SZ /d 0 /f"
        ),
        (
            "19 🧲 Teclado Rápido",
            "Reduz atraso de repetição do teclado.",
            "reg add HKCU\\Control Panel\\Keyboard /v KeyboardDelay /t REG_SZ /d 0 /f"
        ),
        (
            "20 📉 Nagle OFF",
            "Reduz latência em jogos online.",
            "reg add HKLM\\SYSTEM\\CurrentControlSet\\Services\\Tcpip\\Parameters\\Interfaces /v TcpAckFrequency /t REG_DWORD /d 1 /f"
        ),
        (
            "21 🛑 OneDrive OFF",
            "Finaliza o OneDrive para reduzir uso de recursos.",
            "taskkill /f /im OneDrive.exe"
        ),
        (
            "22 📡 Wi-Fi Power OFF",
            "Desativa economia de energia do Wi-Fi.",
            "powercfg -setacvalueindex SCHEME_CURRENT SUB_WIFI POWERSAVINGMODE 0"
        ),
        (
            "23 🧱 Defender CPU Low",
            "Limita uso de CPU do Windows Defender.",
            "powershell Set-MpPreference -ScanAvgCPULoadFactor 5"
        ),
        (
            "24 🔄 Prefetch ON",
            "Melhora carregamento de apps e jogos.",
            "reg add HKLM\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management\\PrefetchParameters /v EnablePrefetcher /t REG_DWORD /d 3 /f"
        ),
        (
            "25 🚀 Full Performance",
            "Ativa todas as configurações de alto desempenho.",
            "powercfg /setactive SCHEME_MIN"
        ),
    ]

    for nome, desc, cmd in otim:
        ctk.CTkButton(
            f,
            text=nome,
            height=42,
            command=lambda n=nome, d=desc, c=cmd: self.confirmar_otimizacao(n, d, c)
        ).pack(fill="x", pady=4)

    return f
# ===============================
    # LIMPEZA
    # ===============================
    def limpeza(self):
        f = ctk.CTkFrame(self.container)

        self.log = ctk.CTkTextbox(f, height=350)
        self.log.pack(fill="both", expand=True)

        ctk.CTkButton(
            f,
            text="🧠 Limpar Memória RAM",
            height=45,
            command=self.limpar_ram
        ).pack(pady=10)

        return f

    # ===============================
    # JOGOS
    # ===============================
    def jogos(self):
        f = ctk.CTkFrame(self.container)

        ctk.CTkLabel(f, text="🎮 Jogos", font=("Segoe UI", 20, "bold")).pack(anchor="w", pady=10)

        ctk.CTkButton(
            f,
            text="🎯 Otimizar Roblox",
            height=45,
            command=lambda: executar("powercfg /setactive SCHEME_MIN")
        ).pack(fill="x", pady=6)

        return f

    # ===============================
    # CONFIG
    # ===============================
    def config(self):
        f = ctk.CTkFrame(self.container)

        ctk.CTkLabel(f, text="⚙️ Configurações", font=("Segoe UI", 20, "bold")).pack(anchor="w", pady=10)

        ctk.CTkOptionMenu(
            f,
            values=["Dark", "Light", "System"],
            command=ctk.set_appearance_mode
        ).pack(anchor="w", pady=10)

        return f

    # ===============================
    # FUNÇÕES (ALINHADAS COM A CLASSE)
    # ===============================
    def limpar_ram(self):
        def t():
            self.log.insert("end", "Limpando RAM...\n")
            limpar_memoria_ram()
            self.log.insert("end", "RAM otimizada com sucesso!\n")
        threading.Thread(target=t, daemon=True).start()

    def modo_turbo(self):
        executar("powercfg /setactive SCHEME_MIN")
        messagebox.showinfo("PyOptiFlow", "🔥 Modo Turbo Ativado!")

    def monitorar(self):
        while True:
            try:
                self.cpu.configure(text=f"{psutil.cpu_percent()}%")
                self.ram.configure(text=f"{psutil.virtual_memory().percent}%")
                self.disk.configure(text=f"{psutil.disk_usage('/').percent}%")
            except:
                pass
            time.sleep(1)

# ===============================
# START (FORA DA CLASSE - SEM ESPAÇOS NO INÍCIO)
# ===============================
if __name__ == "__main__":
    app = PyOptiFlowApp()
    app.mainloop()