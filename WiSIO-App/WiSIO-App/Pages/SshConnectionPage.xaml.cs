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
    }
}
