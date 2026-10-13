using System;
using System.Diagnostics;
using System.IO;
using System.Windows.Forms;

internal static class ElysiaDesktopLauncher
{
    [STAThread]
    private static void Main()
    {
        string desktop = AppDomain.CurrentDomain.BaseDirectory;
        string project = Path.Combine(desktop, "爱莉希雅", "dsh-pet-main", "elysia-desktop-pet");
        string python = Path.Combine(project, ".venv", "Scripts", "pythonw.exe");
        string main = Path.Combine(project, "main.py");
        string setup = Path.Combine(project, "run.bat");

        try
        {
            if (!File.Exists(main))
                throw new FileNotFoundException("找不到桌宠程序：" + main);

            ProcessStartInfo info;
            if (File.Exists(python))
            {
                info = new ProcessStartInfo(python, "\"" + main + "\"");
                info.UseShellExecute = false;
                info.CreateNoWindow = true;
            }
            else if (File.Exists(setup))
            {
                info = new ProcessStartInfo("cmd.exe", "/c \"" + setup + "\"");
                info.UseShellExecute = false;
            }
            else
            {
                throw new FileNotFoundException("找不到桌宠启动文件：" + setup);
            }

            info.WorkingDirectory = project;
            Process.Start(info);
        }
        catch (Exception error)
        {
            MessageBox.Show(error.Message, "爱莉希雅桌宠启动失败",
                MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
    }
}
