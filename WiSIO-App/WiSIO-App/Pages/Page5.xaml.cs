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
using HandyControl.Tools.Extension;

namespace WiSIO_App.Pages
{
    /// <summary>
    /// Interaction logic for Page5.xaml
    /// </summary>
    public partial class Page5 : Page
    {
        public Page5()
        {
            InitializeComponent();
          
        }

        public void GenerateResults()
        {
           
        }

        private void Button_OnClick(object sender, RoutedEventArgs e)
        {
            var bi3 = new BitmapImage();
            bi3.BeginInit();
            bi3.UriSource = new Uri(Properties.Settings.Default.Image1, UriKind.Absolute);
            bi3.EndInit();
            TargetBorder.Background = new ImageBrush(bi3);
            var bi4 = new BitmapImage();
            bi4.BeginInit();
            bi4.UriSource = new Uri(Properties.Settings.Default.Image2, UriKind.Absolute);
            bi4.EndInit();
            SourceBorder.Background = new ImageBrush(bi4);

            ImageViewer.ImageSource = BitmapFrame.Create(new Uri(ProjectSourcePath.Value +"tresholding\\boards\\final_board.png", UriKind.Absolute));
        }
    }
}
