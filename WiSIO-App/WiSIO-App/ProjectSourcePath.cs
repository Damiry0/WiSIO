using System.Runtime.CompilerServices;

namespace WiSIO_App
{
    internal static class ProjectSourcePath
    {
        private static string GetSourceFilePathName( [CallerFilePath] string? callerFilePath = null ) //
            => callerFilePath ?? "";
        private const  string  myRelativePath = nameof(ProjectSourcePath) + ".cs";
        private static string? lazyValue;
        public  static string  Value => lazyValue ??= calculatePath();

        private static string calculatePath()
        {
            string pathName = GetSourceFilePathName();
            return pathName.Substring( 0, pathName.Length - myRelativePath.Length );
        }
    }
}
