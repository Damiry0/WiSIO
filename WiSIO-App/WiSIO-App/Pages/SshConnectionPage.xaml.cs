using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using HandyControl.Controls;
using Renci.SshNet;

namespace WiSIO_App.Pages
{
    /// <summary>
    /// Interaction logic for SshConnectionPage.xaml
    /// </summary>
    public partial class SshConnectionPage : Page
    {
        private bool serverStatus = true;
        public SshConnectionPage()
        {
            InitializeComponent();
        }

        private void CheckConnection_OnClick(object sender, RoutedEventArgs e)
        {
            try
            {
                using (var client = new SshClient(IpBox.Text, 22, LoginBox.Text, PasswordBox.Password)) {
                    client.Connect();

                    if (client.IsConnected) {
                        Growl.Success("Connected successfully!");
                        Properties.Settings.Default.ip = IpBox.Text;
                        Properties.Settings.Default.login = LoginBox.Text;
                        Properties.Settings.Default.password = PasswordBox.Password;
                        Properties.Settings.Default.Save();

                    } else {
                        Growl.WarningGlobal("Connection failed!");
                    }
                    client.Disconnect();
                }
            }
            catch
            {
                Growl.Warning("Connection failed!");
            }
            
        }

        private void TurnOnOffButton_OnClick(object sender, RoutedEventArgs e)
        {
            if (serverStatus)
            {
                try
                {

                    using (var client = new SshClient(Properties.Settings.Default.ip, Properties.Settings.Default.login,
                               Properties.Settings.Default.password))
                    {
                        client.Connect();
                        client.RunCommand("nohup python -u rpi_camera.py </dev/null &>/dev/null & ");
                        client.Disconnect();
                    }

                    WebBrowser.Source = new Uri("http://192.168.1.14:8000/index.html");
                    WebBrowser.Reload();
                    TurnOnOffButton.Content = "Wyłącz Podgląd";
                    serverStatus = false;

                }
                catch
                {
                    Growl.Warning("Connection failed!");
                }
            }
            else
            {
                try
                {
                        using (var client = new SshClient(Properties.Settings.Default.ip, Properties.Settings.Default.login,
                                   Properties.Settings.Default.password))
                        {
                            client.Connect();
                            client.RunCommand("kill -9 `pgrep -f rpi_camera.py`");
                            client.Disconnect();
                        }
                        TurnOnOffButton.Content = "Włacz Podgląd";
                        serverStatus = true;
                }
                catch (Exception exception) {
                        Growl.Warning("Connection failed!");
                }
                
            }

        }
    }
}
